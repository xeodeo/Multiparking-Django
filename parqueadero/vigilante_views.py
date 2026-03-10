import math
import re
from datetime import datetime, timedelta

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from cupones.models import CuponAplicado
from pagos.models import Pago
from reservas.models import Reserva
from tarifas.models import Tarifa
from usuarios.mixins import VigilanteRequiredMixin
from vehiculos.models import Vehiculo

from .models import Espacio, InventarioParqueo, Piso


def _calcular_pisos_data(now):
    """Comparte la lógica de Vista General de Pisos con el admin dashboard."""
    limite_2h = now + timedelta(hours=2)
    pisos = Piso.objects.filter(pisEstado=True).prefetch_related(
        'espacios', 'espacios__reservas'
    ).order_by('pisNombre')

    pisos_list = []
    for piso in pisos:
        total_piso = piso.espacios.count()
        ocupados_piso = piso.espacios.filter(espEstado='OCUPADO').count()
        piso.ocupacion_pct = int((ocupados_piso / total_piso) * 100) if total_piso > 0 else 0
        piso.total_espacios = total_piso
        piso.ocupados_espacios = ocupados_piso

        espacios_list = []
        for espacio in piso.espacios.all():
            reserva_proxima = None
            pago_pendiente = False

            for reserva in espacio.reservas.filter(resEstado__in=['PENDIENTE', 'CONFIRMADA']):
                fhr = datetime.combine(reserva.resFechaReserva, reserva.resHoraInicio)
                fhr = timezone.make_aware(fhr)
                if now <= fhr <= limite_2h:
                    reserva_proxima = reserva
                    break

            if espacio.espEstado == 'OCUPADO':
                pago_pendiente = Pago.objects.filter(
                    fkIdParqueo__fkIdEspacio=espacio,
                    fkIdParqueo__parHoraSalida__isnull=True,
                    pagEstado='PENDIENTE',
                    pagMetodo='EFECTIVO',
                ).exists()

            espacio.reserva_proxima = reserva_proxima
            espacio.pago_pendiente = pago_pendiente
            espacios_list.append(espacio)

        piso.espacios_list = espacios_list
        pisos_list.append(piso)
    return pisos_list


# ── Dashboard ────────────────────────────────────────────────────

class VigilanteDashboardView(VigilanteRequiredMixin, View):
    def get(self, request):
        now = timezone.now()
        hoy_local = timezone.localtime(now).date()

        inicio_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.min.time()))
        fin_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))

        # Stats
        entradas_pendientes = Reserva.objects.filter(
            resFechaReserva=hoy_local,
            resEstado__in=['PENDIENTE', 'CONFIRMADA'],
        ).count()

        salidas_pendientes = InventarioParqueo.objects.filter(
            parHoraSalida__isnull=True,
            pagos__pagEstado='PENDIENTE',
            pagos__pagMetodo='EFECTIVO',
        ).distinct().count()

        efectivo_pendiente = Pago.objects.filter(
            pagEstado='PENDIENTE',
            pagMetodo='EFECTIVO',
            fkIdParqueo__parHoraSalida__isnull=True,
        ).count()

        activos_hoy = InventarioParqueo.objects.filter(
            parHoraEntrada__range=(inicio_hoy, fin_hoy)
        ).count()

        # Búsqueda
        q = request.GET.get('q', '').strip()

        # Solicitudes de Entrada = reservas hoy pendientes/confirmadas
        qs_entrada = Reserva.objects.filter(
            resFechaReserva=hoy_local,
            resEstado__in=['PENDIENTE', 'CONFIRMADA'],
        ).select_related('fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso').order_by('resHoraInicio')

        if q:
            qs_entrada = qs_entrada.filter(
                Q(fkIdVehiculo__vehPlaca__icontains=q) |
                Q(fkIdVehiculo__fkIdUsuario__usuNombre__icontains=q) |
                Q(fkIdVehiculo__fkIdUsuario__usuApellido__icontains=q)
            )

        # Solicitudes de Salida = vehículos con pago pendiente en efectivo
        qs_salida = InventarioParqueo.objects.filter(
            parHoraSalida__isnull=True,
            pagos__pagEstado='PENDIENTE',
            pagos__pagMetodo='EFECTIVO',
        ).distinct().select_related(
            'fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso', 'fkIdEspacio__fkIdTipoEspacio'
        ).order_by('-parHoraEntrada')

        if q:
            qs_salida = qs_salida.filter(
                Q(fkIdVehiculo__vehPlaca__icontains=q) |
                Q(fkIdVehiculo__fkIdUsuario__usuNombre__icontains=q) |
                Q(fkIdVehiculo__fkIdUsuario__usuApellido__icontains=q) |
                Q(fkIdVehiculo__nombre_contacto__icontains=q)
            )

        solicitudes_salida = list(qs_salida)
        for reg in solicitudes_salida:
            reg.pago_pendiente_obj = Pago.objects.filter(
                fkIdParqueo=reg, pagEstado='PENDIENTE', pagMetodo='EFECTIVO'
            ).first()
            if reg.pago_pendiente_obj:
                reg.costo_estimado = float(reg.pago_pendiente_obj.pagMonto)
            else:
                tarifa = Tarifa.objects.filter(
                    fkIdTipoEspacio=reg.fkIdEspacio.fkIdTipoEspacio, activa=True
                ).first()
                if tarifa:
                    total_minutos = max((int((now - reg.parHoraEntrada).total_seconds()) + 59) // 60, 1)
                    es_visitante = reg.fkIdVehiculo.es_visitante
                    precio = float(tarifa.precioHoraVisitante) if es_visitante and tarifa.precioHoraVisitante > 0 else float(tarifa.precioHora)
                    reg.costo_estimado = math.ceil((precio / 60) * total_minutos)
                else:
                    reg.costo_estimado = 0
            reg.costo_display = f"${reg.costo_estimado:,.0f}"

        # Vista General de Pisos
        pisos_list = _calcular_pisos_data(now)

        # Espacios disponibles para ingreso rápido
        espacios_disponibles = Espacio.objects.filter(
            espEstado='DISPONIBLE'
        ).select_related('fkIdPiso', 'fkIdTipoEspacio').order_by('fkIdPiso__pisNombre', 'espNumero')

        return render(request, 'vigilante/dashboard.html', {
            'active_page': 'dashboard',
            'entradas_pendientes': entradas_pendientes,
            'salidas_pendientes': salidas_pendientes,
            'efectivo_pendiente': efectivo_pendiente,
            'activos_hoy': activos_hoy,
            'solicitudes_entrada': qs_entrada,
            'solicitudes_salida': solicitudes_salida,
            'pisos': pisos_list,
            'espacios_disponibles': espacios_disponibles,
            'q': q,
        })


# ── Registrar Ingreso ─────────────────────────────────────────────

class VigilanteRegistrarIngresoView(VigilanteRequiredMixin, View):
    def post(self, request):
        reserva_id = request.POST.get('reserva_id')

        if reserva_id:
            # Entrada desde reserva
            reserva = get_object_or_404(Reserva, pk=reserva_id)
            vehiculo = reserva.fkIdVehiculo
            espacio = reserva.fkIdEspacio

            if espacio.espEstado != 'DISPONIBLE':
                messages.error(request, f'El espacio {espacio.espNumero} no está disponible.')
                return redirect('guardia_dashboard')

            if InventarioParqueo.objects.filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
                messages.error(request, f'El vehículo {vehiculo.vehPlaca} ya tiene un ingreso activo.')
                return redirect('guardia_dashboard')

            InventarioParqueo.objects.create(fkIdVehiculo=vehiculo, fkIdEspacio=espacio)
            espacio.espEstado = 'OCUPADO'
            espacio.save()
            reserva.resEstado = 'COMPLETADA'
            reserva.save()
            messages.success(request, f'Entrada permitida: {vehiculo.vehPlaca} → {espacio.fkIdPiso.pisNombre} #{espacio.espNumero}.')
        else:
            # Entrada directa (visitante / usuario sin reserva)
            placa = request.POST.get('placa', '').upper().strip()
            espacio_id = request.POST.get('espacio_id', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            telefono = request.POST.get('telefono', '').strip()

            if not placa or not espacio_id:
                messages.error(request, 'Placa y espacio son obligatorios.')
                return redirect('guardia_dashboard')

            if not re.match(r'^[A-Za-z0-9-]+$', placa):
                messages.error(request, 'La placa solo acepta letras, números y guiones.')
                return redirect('guardia_dashboard')

            if nombre and not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
                messages.error(request, 'El nombre solo debe contener letras.')
                return redirect('guardia_dashboard')

            if telefono and not re.match(r'^[0-9]+$', telefono):
                messages.error(request, 'El teléfono solo debe contener números.')
                return redirect('guardia_dashboard')

            espacio = get_object_or_404(Espacio, pk=espacio_id)
            if espacio.espEstado != 'DISPONIBLE':
                messages.error(request, f'El espacio {espacio.espNumero} no está disponible.')
                return redirect('guardia_dashboard')

            vehiculo = Vehiculo.objects.filter(vehPlaca=placa).first()
            if not vehiculo:
                vehiculo = Vehiculo.objects.create(
                    vehPlaca=placa,
                    vehTipo='Carro',
                    nombre_contacto=nombre,
                    telefono_contacto=telefono,
                )
            else:
                if vehiculo.es_visitante and (nombre or telefono):
                    if nombre:
                        vehiculo.nombre_contacto = nombre
                    if telefono:
                        vehiculo.telefono_contacto = telefono
                    vehiculo.save()

            if InventarioParqueo.objects.filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
                messages.error(request, f'El vehículo {placa} ya tiene un ingreso activo.')
                return redirect('guardia_dashboard')

            InventarioParqueo.objects.create(fkIdVehiculo=vehiculo, fkIdEspacio=espacio)
            espacio.espEstado = 'OCUPADO'
            espacio.save()
            messages.success(request, f'Ingreso registrado: {placa} → {espacio.fkIdPiso.pisNombre} #{espacio.espNumero}.')

        return redirect('guardia_dashboard')


# ── Registrar Salida ──────────────────────────────────────────────

class VigilanteRegistrarSalidaView(VigilanteRequiredMixin, View):
    def post(self, request):
        registro_id = request.POST.get('registro_id')
        espacio_id = request.POST.get('espacio_id')

        if registro_id:
            registro = get_object_or_404(InventarioParqueo, pk=registro_id, parHoraSalida__isnull=True)
            espacio = registro.fkIdEspacio
        elif espacio_id:
            espacio = get_object_or_404(Espacio, pk=espacio_id)
            registro = InventarioParqueo.objects.filter(
                fkIdEspacio=espacio, parHoraSalida__isnull=True
            ).first()
            if not registro:
                espacio.espEstado = 'DISPONIBLE'
                espacio.save()
                messages.warning(request, f'Espacio {espacio.espNumero} liberado (sin registro activo).')
                return redirect('guardia_dashboard')
        else:
            messages.error(request, 'Datos inválidos.')
            return redirect('guardia_dashboard')

        ahora = timezone.now()
        registro.parHoraSalida = ahora
        registro.save()

        pago_existente = Pago.objects.filter(fkIdParqueo=registro, pagEstado='PENDIENTE').first()
        if pago_existente:
            pago_existente.pagEstado = 'PAGADO'
            pago_existente.save()
            monto = pago_existente.pagMonto
        else:
            tarifa = Tarifa.objects.filter(
                fkIdTipoEspacio=espacio.fkIdTipoEspacio, activa=True
            ).first()
            monto = 0
            if tarifa:
                total_minutos = max((int((ahora - registro.parHoraEntrada).total_seconds()) + 59) // 60, 1)
                vehiculo = registro.fkIdVehiculo
                precio = tarifa.precioHoraVisitante if vehiculo.es_visitante and tarifa.precioHoraVisitante > 0 else tarifa.precioHora
                monto = math.ceil((float(precio) / 60) * total_minutos)
                Pago.objects.create(
                    pagMonto=monto,
                    pagMetodo='EFECTIVO',
                    pagEstado='PAGADO',
                    fkIdParqueo=registro,
                )

        espacio.espEstado = 'DISPONIBLE'
        espacio.save()
        messages.success(
            request,
            f'Salida autorizada: {registro.fkIdVehiculo.vehPlaca}. Cobro: ${float(monto):,.0f} COP'
        )
        return redirect('guardia_dashboard')


# ── Confirmar Pago en Efectivo ────────────────────────────────────

class VigilanteConfirmarPagoView(VigilanteRequiredMixin, View):
    def post(self, request):
        registro_id = request.POST.get('registro_id')
        registro = get_object_or_404(InventarioParqueo, pk=registro_id)

        pago = Pago.objects.filter(fkIdParqueo=registro, pagEstado='PENDIENTE').first()
        if not pago:
            messages.error(request, 'No se encontró pago pendiente para este vehículo.')
            return redirect('guardia_dashboard')

        pago.pagEstado = 'PAGADO'
        pago.save()
        messages.success(
            request,
            f'Pago confirmado: {registro.fkIdVehiculo.vehPlaca} — ${float(pago.pagMonto):,.0f} COP'
        )
        return redirect('guardia_dashboard')


# ── Buscar Vehículo (AJAX) ────────────────────────────────────────

class VigilanteBuscarVehiculoView(VigilanteRequiredMixin, View):
    def get(self, request):
        placa = request.GET.get('placa', '').upper().strip()
        if not placa:
            return JsonResponse({'error': 'Placa requerida'}, status=400)

        vehiculo = Vehiculo.objects.filter(vehPlaca=placa).first()
        if vehiculo:
            return JsonResponse({
                'found': True,
                'es_visitante': vehiculo.es_visitante,
                'nombre': vehiculo.nombre_contacto or (vehiculo.fkIdUsuario.usuNombreCompleto if vehiculo.fkIdUsuario else ''),
                'telefono': vehiculo.telefono_contacto or (vehiculo.fkIdUsuario.usuTelefono if vehiculo.fkIdUsuario else ''),
            })
        return JsonResponse({'found': False})


# ── Detalle de Ocupación (AJAX) ───────────────────────────────────

class VigilanteObtenerDetalleView(VigilanteRequiredMixin, View):
    def get(self, request):
        espacio_id = request.GET.get('espacio_id')
        if not espacio_id:
            return JsonResponse({'error': 'ID requerido'}, status=400)

        try:
            espacio = get_object_or_404(Espacio, pk=espacio_id)
            registro = InventarioParqueo.objects.select_related(
                'fkIdVehiculo__fkIdUsuario',
                'fkIdEspacio__fkIdPiso',
                'fkIdEspacio__fkIdTipoEspacio',
            ).filter(fkIdEspacio=espacio, parHoraSalida__isnull=True).first()

            if not registro:
                return JsonResponse({'found': False})

            now = timezone.now()
            entrada = registro.parHoraEntrada
            total_minutos = max((int((now - entrada).total_seconds()) + 59) // 60, 1)
            dias = total_minutos // 1440
            horas = (total_minutos % 1440) // 60
            minutos = total_minutos % 60
            partes = []
            if dias:
                partes.append(f'{dias}d')
            if horas:
                partes.append(f'{horas}h')
            partes.append(f'{minutos}m')
            duracion_str = ' '.join(partes)

            pago_pendiente = Pago.objects.filter(
                fkIdParqueo=registro, pagEstado='PENDIENTE'
            ).first()

            tarifa = Tarifa.objects.filter(
                fkIdTipoEspacio=espacio.fkIdTipoEspacio, activa=True
            ).first()

            subtotal = 0
            tarifa_info = 'Sin tarifa configurada'
            precio_hora_num = 0
            if tarifa:
                vehiculo = registro.fkIdVehiculo
                precio_hora_num = float(tarifa.precioHoraVisitante) if vehiculo.es_visitante and tarifa.precioHoraVisitante > 0 else float(tarifa.precioHora)
                subtotal = math.ceil((precio_hora_num / 60) * total_minutos)
                tarifa_info = f'${precio_hora_num:,.0f} / Hora' + (' (Visitante)' if vehiculo.es_visitante else '')

            total_pagar = float(pago_pendiente.pagMonto) if pago_pendiente else subtotal
            vehiculo = registro.fkIdVehiculo
            usuario = vehiculo.fkIdUsuario

            return JsonResponse({
                'found': True,
                'registro_id': registro.pk,
                'placa': vehiculo.vehPlaca,
                'tipo_vehiculo': vehiculo.vehTipo,
                'tipo_espacio': espacio.fkIdTipoEspacio.nombre,
                'hora_entrada': timezone.localtime(entrada).strftime('%d/%m/%Y %I:%M %p'),
                'duracion': duracion_str,
                'cliente': usuario.usuNombreCompleto if usuario else (vehiculo.nombre_contacto or 'Visitante'),
                'tipo_cliente': 'USUARIO' if usuario else 'VISITANTE',
                'telefono': usuario.usuTelefono if usuario else (vehiculo.telefono_contacto or 'Sin teléfono'),
                'tarifa_info': tarifa_info,
                'total_pagar': f'${total_pagar:,.0f}',
                'tiene_pago_pendiente': pago_pendiente is not None,
                'entrada_iso': timezone.localtime(entrada).isoformat(),
                'precio_hora': precio_hora_num,
                'piso': espacio.fkIdPiso.pisNombre,
                'espacio_numero': espacio.espNumero,
            })
        except Exception as e:
            return JsonResponse({'found': False, 'error': str(e)}, status=500)


# ── Dashboard Data API (auto-refresh) ────────────────────────────

class VigilanteDashboardDataView(VigilanteRequiredMixin, View):
    def get(self, request):
        now = timezone.now()
        hoy_local = timezone.localtime(now).date()
        inicio_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.min.time()))
        fin_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))

        entradas_pendientes = Reserva.objects.filter(
            resFechaReserva=hoy_local, resEstado__in=['PENDIENTE', 'CONFIRMADA']
        ).count()
        salidas_pendientes = InventarioParqueo.objects.filter(
            parHoraSalida__isnull=True,
            pagos__pagEstado='PENDIENTE',
            pagos__pagMetodo='EFECTIVO',
        ).distinct().count()
        efectivo_pendiente = Pago.objects.filter(
            pagEstado='PENDIENTE', pagMetodo='EFECTIVO',
            fkIdParqueo__parHoraSalida__isnull=True,
        ).count()
        activos_hoy = InventarioParqueo.objects.filter(
            parHoraEntrada__range=(inicio_hoy, fin_hoy)
        ).count()

        return JsonResponse({
            'entradas_pendientes': entradas_pendientes,
            'salidas_pendientes': salidas_pendientes,
            'efectivo_pendiente': efectivo_pendiente,
            'activos_hoy': activos_hoy,
        })
