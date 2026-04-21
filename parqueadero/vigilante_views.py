import math
import re
from datetime import datetime, timedelta

from django.contrib import messages
from django.db import transaction
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

from multiparking import email_utils
from fidelidad.models import Sticker
from .models import Espacio, InventarioParqueo, Piso
from .services import calcular_costo_parqueo, STICKER_MIN_MINUTOS
from .utils import _calcular_pisos_data


# ── Dashboard ────────────────────────────────────────────────────

class VigilanteDashboardView(VigilanteRequiredMixin, View):
    def get(self, request):
        now = timezone.now()
        hoy_local = timezone.localtime(now).date()

        # Rango completo del día local para filtrar entradas de hoy
        inicio_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.min.time()))
        fin_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))

        # ── KPIs del encabezado ──────────────────────────────────────
        # Reservas de hoy que aún no se han procesado (pendientes de entrada)
        entradas_pendientes = Reserva.objects.filter(
            resFechaReserva=hoy_local,
            resEstado__in=['PENDIENTE', 'CONFIRMADA'],
        ).count()

        # Vehículos activos con pago en efectivo pendiente de cobrar
        salidas_pendientes = InventarioParqueo.objects.filter(
            parHoraSalida__isnull=True,
            pagos__pagEstado='PENDIENTE',
            pagos__pagMetodo='EFECTIVO',
        ).distinct().count()

        # Total de registros de pago en efectivo sin confirmar
        efectivo_pendiente = Pago.objects.filter(
            pagEstado='PENDIENTE',
            pagMetodo='EFECTIVO',
            fkIdParqueo__parHoraSalida__isnull=True,
        ).count()

        # Vehículos que ingresaron en algún momento hoy
        activos_hoy = InventarioParqueo.objects.filter(
            parHoraEntrada__range=(inicio_hoy, fin_hoy)
        ).count()

        # Término de búsqueda opcional (filtra por placa o nombre)
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
            # Si ya existe un pago pre-calculado, usar ese monto
            reg.pago_pendiente_obj = Pago.objects.filter(
                fkIdParqueo=reg, pagEstado='PENDIENTE', pagMetodo='EFECTIVO'
            ).first()
            if reg.pago_pendiente_obj:
                reg.costo_estimado = float(reg.pago_pendiente_obj.pagMonto)
            else:
                # Si no hay pago previo, calcular en tiempo real según la tarifa activa
                tarifa = Tarifa.get_active_for(reg.fkIdEspacio.fkIdTipoEspacio)
                if tarifa:
                    reg.costo_estimado = calcular_costo_parqueo(reg.parHoraEntrada, tarifa, reg.fkIdVehiculo)
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

        with transaction.atomic():
            if reserva_id:
                # ── Flujo 1: Entrada desde una reserva existente ──────────
                reserva = get_object_or_404(Reserva, pk=reserva_id)
                vehiculo = reserva.fkIdVehiculo
                espacio = reserva.fkIdEspacio

                # Verifica que el espacio no haya sido ocupado por otro vehículo
                if espacio.espEstado != 'DISPONIBLE':
                    messages.error(request, f'El espacio {espacio.espNumero} no está disponible.')
                    return redirect('guardia_dashboard')

                # Evita doble ingreso del mismo vehículo
                if InventarioParqueo.objects.select_for_update().filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
                    messages.error(request, f'El vehículo {vehiculo.vehPlaca} ya tiene un ingreso activo.')
                    return redirect('guardia_dashboard')

                # Crea el registro de parqueo, ocupa el espacio y cierra la reserva
                nuevo_registro = InventarioParqueo.objects.create(fkIdVehiculo=vehiculo, fkIdEspacio=espacio)
                email_utils.enviar_confirmacion_entrada(nuevo_registro)
                espacio.ocupar()
                reserva.resEstado = 'COMPLETADA'
                reserva.save()
                messages.success(request, f'Entrada permitida: {vehiculo.vehPlaca} → {espacio.fkIdPiso.pisNombre} #{espacio.espNumero}.')
            else:
                # ── Flujo 2: Ingreso rápido (visitante o usuario sin reserva) ──
                placa = request.POST.get('placa', '').upper().strip()
                espacio_id = request.POST.get('espacio_id', '').strip()
                nombre = request.POST.get('nombre', '').strip()
                telefono = request.POST.get('telefono', '').strip()

                # Campos obligatorios
                if not placa or not espacio_id:
                    messages.error(request, 'Placa y espacio son obligatorios.')
                    return redirect('guardia_dashboard')

                # Validaciones de formato
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

                # Busca el vehículo en BD; si no existe, lo crea como visitante (sin usuario)
                vehiculo = Vehiculo.objects.filter(vehPlaca=placa).first()
                if not vehiculo:
                    vehiculo = Vehiculo.objects.create(
                        vehPlaca=placa,
                        vehTipo='Carro',
                        nombre_contacto=nombre,
                        telefono_contacto=telefono,
                    )
                else:
                    # Si el vehículo es visitante y se ingresaron datos de contacto, actualizarlos
                    if vehiculo.es_visitante and (nombre or telefono):
                        if nombre:
                            vehiculo.nombre_contacto = nombre
                        if telefono:
                            vehiculo.telefono_contacto = telefono
                        vehiculo.save()

                # Evita doble ingreso
                if InventarioParqueo.objects.select_for_update().filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
                    messages.error(request, f'El vehículo {placa} ya tiene un ingreso activo.')
                    return redirect('guardia_dashboard')

                # Crea el registro de parqueo y ocupa el espacio
                nuevo_registro = InventarioParqueo.objects.create(fkIdVehiculo=vehiculo, fkIdEspacio=espacio)
                email_utils.enviar_confirmacion_entrada(nuevo_registro)
                espacio.ocupar()
                messages.success(request, f'Ingreso registrado: {placa} → {espacio.fkIdPiso.pisNombre} #{espacio.espNumero}.')

        return redirect('guardia_dashboard')


# ── Registrar Salida ──────────────────────────────────────────────

class VigilanteRegistrarSalidaView(VigilanteRequiredMixin, View):
    def post(self, request):
        registro_id = request.POST.get('registro_id')
        espacio_id = request.POST.get('espacio_id')

        with transaction.atomic():
            # Acepta identificar el registro por ID de inventario o por ID de espacio
            if registro_id:
                registro = get_object_or_404(InventarioParqueo, pk=registro_id, parHoraSalida__isnull=True)
                espacio = registro.fkIdEspacio
            elif espacio_id:
                espacio = get_object_or_404(Espacio, pk=espacio_id)
                # Busca el registro activo (sin hora de salida) de este espacio
                registro = InventarioParqueo.objects.filter(
                    fkIdEspacio=espacio, parHoraSalida__isnull=True
                ).first()
                if not registro:
                    # No hay registro activo; liberar el espacio de todas formas
                    espacio.liberar()
                    messages.warning(request, f'Espacio {espacio.espNumero} liberado (sin registro activo).')
                    return redirect('guardia_dashboard')
            else:
                messages.error(request, 'Datos inválidos.')
                return redirect('guardia_dashboard')

            # Registra la hora de salida
            ahora = timezone.now()
            registro.parHoraSalida = ahora
            registro.save()

            # ── Cobro ────────────────────────────────────────────────────
            pago_existente = Pago.objects.filter(fkIdParqueo=registro, pagEstado='PENDIENTE').first()
            if pago_existente:
                # Ya existe un pago pre-calculado (ej: generado al momento del ingreso); solo confirmarlo
                pago_existente.pagEstado = 'PAGADO'
                pago_existente.save()
                monto = pago_existente.pagMonto
                if not registro.fkIdVehiculo.es_visitante:
                    email_utils.enviar_recibo_pago(pago_existente, registro)
            else:
                # Calcular el cobro ahora según la tarifa activa del tipo de espacio
                tarifa = Tarifa.get_active_for(espacio.fkIdTipoEspacio)
                monto = 0
                if tarifa:
                    monto = calcular_costo_parqueo(registro.parHoraEntrada, tarifa, registro.fkIdVehiculo, ahora)
                    nuevo_pago = Pago.objects.create(
                        pagMonto=monto,
                        pagMetodo='EFECTIVO',
                        pagEstado='PAGADO',
                        fkIdParqueo=registro,
                    )
                    if not registro.fkIdVehiculo.es_visitante:
                        email_utils.enviar_recibo_pago(nuevo_pago, registro)

            # Sticker de fidelidad: si estuvo más de 1 hora y es usuario registrado
            usuario_vehiculo = registro.fkIdVehiculo.fkIdUsuario
            if usuario_vehiculo:
                duracion_min = int((ahora - registro.parHoraEntrada).total_seconds()) // 60
                if duracion_min >= STICKER_MIN_MINUTOS:
                    Sticker.objects.get_or_create(
                        fkIdParqueo=registro,
                        defaults={'fkIdUsuario': usuario_vehiculo}
                    )

            # Liberar el espacio para nuevos ingresos
            espacio.liberar()
            messages.success(
                request,
                f'Salida autorizada: {registro.fkIdVehiculo.vehPlaca}. Cobro: ${float(monto):,.0f} COP'
            )
        return redirect('guardia_dashboard')


# ── Confirmar Pago en Efectivo ────────────────────────────────────

class VigilanteConfirmarPagoView(VigilanteRequiredMixin, View):
    """Confirma el cobro en efectivo de un vehículo que aún sigue estacionado."""
    def post(self, request):
        registro_id = request.POST.get('registro_id')
        registro = get_object_or_404(InventarioParqueo, pk=registro_id)

        # Busca el pago pendiente asociado al registro de parqueo
        pago = Pago.objects.filter(fkIdParqueo=registro, pagEstado='PENDIENTE').first()
        if not pago:
            messages.error(request, 'No se encontró pago pendiente para este vehículo.')
            return redirect('guardia_dashboard')

        # Marca el pago como cobrado (el vehículo puede seguir estacionado)
        pago.pagEstado = 'PAGADO'
        pago.save()
        messages.success(
            request,
            f'Pago confirmado: {registro.fkIdVehiculo.vehPlaca} — ${float(pago.pagMonto):,.0f} COP'
        )
        return redirect('guardia_dashboard')


# ── Buscar Vehículo (AJAX) ────────────────────────────────────────

class VigilanteBuscarVehiculoView(VigilanteRequiredMixin, View):
    """Endpoint AJAX para autocompletar datos del vehículo al escribir la placa en el modal de ingreso."""
    def get(self, request):
        placa = request.GET.get('placa', '').upper().strip()
        if not placa:
            return JsonResponse({'error': 'Placa requerida'}, status=400)

        vehiculo = Vehiculo.objects.filter(vehPlaca=placa).first()
        if vehiculo:
            # Retorna datos de contacto: primero los del vehículo, luego los del usuario registrado
            return JsonResponse({
                'found': True,
                'es_visitante': vehiculo.es_visitante,
                'nombre': vehiculo.nombre_contacto or (vehiculo.fkIdUsuario.usuNombreCompleto if vehiculo.fkIdUsuario else ''),
                'telefono': vehiculo.telefono_contacto or (vehiculo.fkIdUsuario.usuTelefono if vehiculo.fkIdUsuario else ''),
            })
        return JsonResponse({'found': False})


# ── Detalle de Ocupación (AJAX) ───────────────────────────────────

class VigilanteObtenerDetalleView(VigilanteRequiredMixin, View):
    """Endpoint AJAX que retorna el detalle completo de un espacio ocupado para el modal de información."""
    def get(self, request):
        espacio_id = request.GET.get('espacio_id')
        if not espacio_id:
            return JsonResponse({'error': 'ID requerido'}, status=400)

        try:
            espacio = get_object_or_404(Espacio, pk=espacio_id)
            # Busca el registro activo (vehículo actualmente estacionado) en este espacio
            registro = InventarioParqueo.objects.select_related(
                'fkIdVehiculo__fkIdUsuario',
                'fkIdEspacio__fkIdPiso',
                'fkIdEspacio__fkIdTipoEspacio',
            ).filter(fkIdEspacio=espacio, parHoraSalida__isnull=True).first()

            if not registro:
                return JsonResponse({'found': False})

            now = timezone.now()
            entrada = registro.parHoraEntrada
            duracion_str = registro.duracion_str(now)

            # Verifica si ya hay un pago pendiente pre-calculado
            pago_pendiente = Pago.objects.filter(
                fkIdParqueo=registro, pagEstado='PENDIENTE'
            ).first()

            tarifa = Tarifa.get_active_for(espacio.fkIdTipoEspacio)

            subtotal = 0
            tarifa_info = 'Sin tarifa configurada'
            precio_hora_num = 0
            if tarifa:
                vehiculo = registro.fkIdVehiculo
                precio_hora_num = float(tarifa.precioHoraVisitante) if vehiculo.es_visitante and tarifa.precioHoraVisitante > 0 else float(tarifa.precioHora)
                subtotal = calcular_costo_parqueo(entrada, tarifa, vehiculo, now)
                tarifa_info = f'${precio_hora_num:,.0f} / Hora' + (' (Visitante)' if vehiculo.es_visitante else '')

            # Si ya hay pago calculado, usar ese monto; si no, usar el estimado en tiempo real
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
                # entrada_iso y precio_hora se usan en el JS para el timer en vivo
                'entrada_iso': timezone.localtime(entrada).isoformat(),
                'precio_hora': precio_hora_num,
                'piso': espacio.fkIdPiso.pisNombre,
                'espacio_numero': espacio.espNumero,
            })
        except Exception as e:
            return JsonResponse({'found': False, 'error': str(e)}, status=500)


# ── Dashboard Data API (auto-refresh) ────────────────────────────

class VigilanteDashboardDataView(VigilanteRequiredMixin, View):
    """
    Endpoint AJAX que el JS llama cada 30 segundos para actualizar el dashboard
    sin recargar la página (KPIs, mapa de pisos y listas de solicitudes).
    """
    def get(self, request):
        now = timezone.now()
        hoy_local = timezone.localtime(now).date()
        inicio_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.min.time()))
        fin_hoy = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))
        limite_2h = now + timedelta(hours=2)

        # ── KPIs ─────────────────────────────────────────────────────
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

        # ── Datos del mapa de pisos ───────────────────────────────────
        pisos = Piso.objects.filter(pisEstado=True).prefetch_related(
            'espacios', 'espacios__reservas'
        ).order_by('pisNombre')

        pisos_data = []
        for piso in pisos:
            total_piso = piso.espacios.count()
            ocupados_piso = piso.espacios.filter(espEstado='OCUPADO').count()
            ocupacion_pct = int((ocupados_piso / total_piso) * 100) if total_piso > 0 else 0

            espacios_data = []
            for espacio in piso.espacios.all():
                reserva_proxima = None
                pago_pendiente = False

                # Detecta reservas que inician en los próximos 2 horas
                for reserva in espacio.reservas.filter(resEstado__in=['PENDIENTE', 'CONFIRMADA']):
                    fhr = datetime.combine(reserva.resFechaReserva, reserva.resHoraInicio)
                    fhr = timezone.make_aware(fhr)
                    if now <= fhr <= limite_2h:
                        reserva_proxima = reserva
                        break

                # Detecta si el espacio ocupado tiene cobro pendiente
                placa_actual = None
                if espacio.espEstado == 'OCUPADO':
                    pago_pendiente = Pago.objects.filter(
                        fkIdParqueo__fkIdEspacio=espacio,
                        fkIdParqueo__parHoraSalida__isnull=True,
                        pagEstado='PENDIENTE',
                        pagMetodo='EFECTIVO',
                    ).exists()
                    registro_activo = InventarioParqueo.objects.filter(
                        fkIdEspacio=espacio,
                        parHoraSalida__isnull=True
                    ).select_related('fkIdVehiculo').first()
                    if registro_activo:
                        placa_actual = registro_activo.fkIdVehiculo.vehPlaca

                espacios_data.append({
                    'pk': espacio.pk,
                    'espNumero': espacio.espNumero,
                    'espEstado': espacio.espEstado,
                    'pago_pendiente': pago_pendiente,
                    'reserva_pk': reserva_proxima.pk if reserva_proxima else None,
                    'placa_actual': placa_actual,
                })

            pisos_data.append({
                'pk': piso.pk,
                'pisNombre': piso.pisNombre,
                'total_espacios': total_piso,
                'ocupados_espacios': ocupados_piso,
                'ocupacion_pct': ocupacion_pct,
                'espacios': espacios_data,
            })

        # ── Solicitudes de Entrada ────────────────────────────────────
        qs_entrada = Reserva.objects.filter(
            resFechaReserva=hoy_local, resEstado__in=['PENDIENTE', 'CONFIRMADA']
        ).select_related('fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso').order_by('resHoraInicio')

        solicitudes_entrada_data = []
        for r in qs_entrada:
            v = r.fkIdVehiculo
            solicitudes_entrada_data.append({
                'pk': r.pk,
                'placa': v.vehPlaca,
                'nombre': v.fkIdUsuario.usuNombreCompleto if v.fkIdUsuario else (v.nombre_contacto or 'Visitante'),
                'piso': r.fkIdEspacio.fkIdPiso.pisNombre,
                'espacio': r.fkIdEspacio.espNumero,
                'hora': r.resHoraInicio.strftime('%H:%M'),
                # Identificador de referencia legible para el guardia
                'ref': f'RES-{r.pk:010d}',
            })

        # ── Solicitudes de Salida ─────────────────────────────────────
        qs_salida = InventarioParqueo.objects.filter(
            parHoraSalida__isnull=True,
            pagos__pagEstado='PENDIENTE',
            pagos__pagMetodo='EFECTIVO',
        ).distinct().select_related(
            'fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso', 'fkIdEspacio__fkIdTipoEspacio'
        ).order_by('-parHoraEntrada')

        solicitudes_salida_data = []
        for reg in qs_salida:
            v = reg.fkIdVehiculo
            pago = Pago.objects.filter(fkIdParqueo=reg, pagEstado='PENDIENTE', pagMetodo='EFECTIVO').first()
            if pago:
                costo = float(pago.pagMonto)
            else:
                # Calcular estimado en tiempo real si no hay pago pre-calculado
                tarifa = Tarifa.get_active_for(reg.fkIdEspacio.fkIdTipoEspacio)
                if tarifa:
                    costo = calcular_costo_parqueo(reg.parHoraEntrada, tarifa, v)
                else:
                    costo = 0
            solicitudes_salida_data.append({
                'pk': reg.pk,
                'placa': v.vehPlaca,
                'nombre': v.fkIdUsuario.usuNombreCompleto if v.fkIdUsuario else (v.nombre_contacto or 'Visitante'),
                'piso': reg.fkIdEspacio.fkIdPiso.pisNombre,
                'espacio': reg.fkIdEspacio.espNumero,
                'hora': timezone.localtime(reg.parHoraEntrada).strftime('%H:%M'),
                'costo': f'${costo:,.0f}',
                'pago_pendiente': pago is not None,
            })

        return JsonResponse({
            'entradas_pendientes': entradas_pendientes,
            'salidas_pendientes': salidas_pendientes,
            'efectivo_pendiente': efectivo_pendiente,
            'activos_hoy': activos_hoy,
            'pisos': pisos_data,
            'solicitudes_entrada': solicitudes_entrada_data,
            'solicitudes_salida': solicitudes_salida_data,
        })
