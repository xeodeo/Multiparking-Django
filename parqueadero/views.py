from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
import json

from reservas.models import Reserva
from usuarios.mixins import AdminRequiredMixin
from pagos.models import Pago
from tarifas.models import Tarifa

from .models import Espacio, Piso, TipoEspacio, InventarioParqueo
from vehiculos.models import Vehiculo

# ── Dashboard ────────────────────────────────────────────────────


# ── Dashboard ────────────────────────────────────────────────────
class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        total = Espacio.objects.count()
        ocupados = Espacio.objects.filter(espEstado='OCUPADO').count()
        disponibles = Espacio.objects.filter(espEstado='DISPONIBLE').count()
        reservas_activas = Reserva.objects.filter(
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        ).count()
        # Solo pisos activos
        pisos = Piso.objects.filter(pisEstado=True).prefetch_related('espacios').order_by('pisNombre')
        
        # Convertir a lista para mantener los atributos calculados y evitar re-evaluación
        pisos_list = []
        for piso in pisos:
            total_piso = piso.espacios.count()
            ocupados_piso = piso.espacios.filter(espEstado='OCUPADO').count()
            piso.ocupacion_pct = int((ocupados_piso / total_piso) * 100) if total_piso > 0 else 0
            piso.total_espacios = total_piso
            piso.ocupados_espacios = ocupados_piso
            pisos_list.append(piso)


        # ── DATOS PARA GRÁFICOS Y TABLAS ──
        
        # 1. Tabla de Reservas Recientes
        reservas_recientes = Reserva.objects.select_related(
            'fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso'
        ).order_by('-resFechaReserva', '-resHoraInicio')[:5]

        # 2. Ingresos por Turno (Hoy) - TIMEZONE AWARE
        now = timezone.now() # Fecha con zona horaria
        hoy_local = timezone.localtime(now).date()
        
        # Definir rangos horarios localizados
        def get_range(start_hour, end_hour):
            start = timezone.make_aware(timezone.datetime.combine(hoy_local, timezone.datetime.min.time().replace(hour=start_hour)))
            end = timezone.make_aware(timezone.datetime.combine(hoy_local, timezone.datetime.min.time().replace(hour=end_hour))) if end_hour < 24 else \
                  timezone.make_aware(timezone.datetime.combine(hoy_local + timezone.timedelta(days=1), timezone.datetime.min.time()))
            return start, end

        start_manana, end_manana = get_range(6, 14)
        start_tarde, end_tarde = get_range(14, 22)
        
        # Noche: 22:00 hoy - 06:00 mañana (pero el grafico dice 'Ingresos por Turno' y usualmente se muestra lo del dia)
        # Interpretación: Noche cubre 00:00-06:00 Y 22:00-23:59 del día actual para reporte diario
        start_noche1, end_noche1 = get_range(0, 6)
        start_noche2, end_noche2 = get_range(22, 24)

        pagos = Pago.objects.filter(pagFechaPago__date=hoy_local, pagEstado='PAGADO')
        
        # Filtro en memoria para evitar complejidad de DB con SQLite/Timezones
        # Es eficiente porque filtramos primero por día
        p_manana = 0
        p_tarde = 0
        p_noche = 0

        for p in pagos:
            p_local = timezone.localtime(p.pagFechaPago)
            h = p_local.hour
            monto = float(p.pagMonto)
            
            if 6 <= h < 14:
                p_manana += monto
            elif 14 <= h < 22:
                p_tarde += monto
            else: # 22-23 o 00-05
                p_noche += monto

        ingresos_data = json.dumps([p_manana, p_tarde, p_noche])

        # 3. Tendencias de Ocupación (Por hora hoy) - TIMEZONE AWARE
        ocupacion_data = []
        labels_horas = []
        
        # Optimización: Traer todos los registros del día y contar en Python
        registros_hoy = InventarioParqueo.objects.filter(
            parHoraEntrada__range=(
                timezone.make_aware(timezone.datetime.combine(hoy_local, timezone.datetime.min.time())),
                timezone.make_aware(timezone.datetime.combine(hoy_local, timezone.datetime.max.time()))
            )
        )
        
        counts_por_hora = {h: 0 for h in range(6, 23)}
        for r in registros_hoy:
            h = timezone.localtime(r.parHoraEntrada).hour
            if 6 <= h < 23:
                counts_por_hora[h] += 1
                
        for h in range(6, 23):
            labels_horas.append(f"{h}:00")
            ocupacion_data.append(counts_por_hora[h])

        return render(request, 'admin_panel/dashboard.html', {
            'active_page': 'dashboard',
            'total_espacios': total,
            'disponibles': disponibles,
            'ocupados': ocupados,
            'reservas_activas': reservas_activas,
            'pisos': pisos_list,
            'reservas_recientes': reservas_recientes,
            'ingresos_data': ingresos_data,
            'ocupacion_data': json.dumps(ocupacion_data),
            'ocupacion_labels': json.dumps(labels_horas),
        })


# ── Pisos CRUD ───────────────────────────────────────────────────
class PisoListView(AdminRequiredMixin, View):
    def get(self, request):
        pisos = Piso.objects.annotate(
            total=Count('espacios'),
            ocupados=Count('espacios', filter=Q(espacios__espEstado='OCUPADO')),
        ).order_by('pk')
        for p in pisos:
            p.libres = p.total - p.ocupados
            p.porcentaje = round(p.ocupados * 100 / p.total) if p.total else 0
        return render(request, 'admin_panel/pisos/list.html', {
            'active_page': 'pisos',
            'pisos': pisos,
        })


class PisoCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/pisos/form.html', {
            'active_page': 'pisos',
            'title': 'Nuevo Piso',
        })

    def post(self, request):
        nombre = request.POST.get('pisNombre', '').strip()
        estado = 'pisEstado' in request.POST
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return render(request, 'admin_panel/pisos/form.html', {
                'active_page': 'pisos',
                'title': 'Nuevo Piso',
            })
        Piso.objects.create(pisNombre=nombre, pisEstado=estado)
        messages.success(request, 'Piso creado exitosamente.')
        return redirect('admin_pisos')


class PisoUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        piso = get_object_or_404(Piso, pk=pk)
        return render(request, 'admin_panel/pisos/form.html', {
            'active_page': 'pisos',
            'title': 'Editar Piso',
            'piso': piso,
        })

    def post(self, request, pk):
        piso = get_object_or_404(Piso, pk=pk)
        nombre = request.POST.get('pisNombre', '').strip()
        estado = 'pisEstado' in request.POST
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return render(request, 'admin_panel/pisos/form.html', {
                'active_page': 'pisos',
                'title': 'Editar Piso',
                'piso': piso,
            })
        piso.pisNombre = nombre
        piso.pisEstado = estado
        piso.save()
        messages.success(request, 'Piso actualizado exitosamente.')
        return redirect('admin_pisos')


class PisoDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        piso = get_object_or_404(Piso, pk=pk)
        if piso.espacios.filter(espEstado='OCUPADO').exists():
            messages.error(request, 'No se puede eliminar: tiene espacios ocupados.')
            return redirect('admin_pisos')
        piso.delete()
        messages.success(request, 'Piso eliminado.')
        return redirect('admin_pisos')


# ── Tipos de Espacio CRUD ────────────────────────────────────────
class TipoEspacioListView(AdminRequiredMixin, View):
    def get(self, request):
        tipos = TipoEspacio.objects.annotate(
            total_espacios=Count('espacios'),
            total_tarifas=Count('tarifas'),
        ).order_by('pk')
        return render(request, 'admin_panel/tipos_espacio/list.html', {
            'active_page': 'tipos_espacio',
            'tipos': tipos,
        })


class TipoEspacioCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/tipos_espacio/form.html', {
            'active_page': 'tipos_espacio',
            'title': 'Nuevo Tipo de Espacio',
        })

    def post(self, request):
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return render(request, 'admin_panel/tipos_espacio/form.html', {
                'active_page': 'tipos_espacio',
                'title': 'Nuevo Tipo de Espacio',
            })
        if TipoEspacio.objects.filter(nombre=nombre).exists():
            messages.error(request, 'Ya existe un tipo con ese nombre.')
            return render(request, 'admin_panel/tipos_espacio/form.html', {
                'active_page': 'tipos_espacio',
                'title': 'Nuevo Tipo de Espacio',
                'tipo': {'nombre': nombre},
            })
        TipoEspacio.objects.create(nombre=nombre)
        messages.success(request, 'Tipo de espacio creado exitosamente.')
        return redirect('admin_tipos_espacio')


class TipoEspacioUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        tipo = get_object_or_404(TipoEspacio, pk=pk)
        return render(request, 'admin_panel/tipos_espacio/form.html', {
            'active_page': 'tipos_espacio',
            'title': 'Editar Tipo de Espacio',
            'tipo': tipo,
        })

    def post(self, request, pk):
        tipo = get_object_or_404(TipoEspacio, pk=pk)
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return render(request, 'admin_panel/tipos_espacio/form.html', {
                'active_page': 'tipos_espacio',
                'title': 'Editar Tipo de Espacio',
                'tipo': tipo,
            })
        if TipoEspacio.objects.filter(nombre=nombre).exclude(pk=pk).exists():
            messages.error(request, 'Ya existe un tipo con ese nombre.')
            return render(request, 'admin_panel/tipos_espacio/form.html', {
                'active_page': 'tipos_espacio',
                'title': 'Editar Tipo de Espacio',
                'tipo': tipo,
            })
        tipo.nombre = nombre
        tipo.save()
        messages.success(request, 'Tipo de espacio actualizado.')
        return redirect('admin_tipos_espacio')


class TipoEspacioDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        tipo = get_object_or_404(TipoEspacio, pk=pk)
        if tipo.espacios.exists():
            messages.error(request, 'No se puede eliminar: tiene espacios asociados.')
            return redirect('admin_tipos_espacio')
        tipo.delete()
        messages.success(request, 'Tipo de espacio eliminado.')
        return redirect('admin_tipos_espacio')


# ── Espacios CRUD ────────────────────────────────────────────────
class EspacioListView(AdminRequiredMixin, View):
    def get(self, request):
        qs = Espacio.objects.select_related('fkIdPiso', 'fkIdTipoEspacio').order_by('espNumero')

        # Filtros
        q = request.GET.get('q', '').strip()
        piso_id = request.GET.get('piso', '')
        tipo_id = request.GET.get('tipo', '')
        estado = request.GET.get('estado', '')

        if q:
            qs = qs.filter(espNumero__icontains=q)
        if piso_id:
            qs = qs.filter(fkIdPiso_id=piso_id)
        if tipo_id:
            qs = qs.filter(fkIdTipoEspacio_id=tipo_id)
        if estado:
            qs = qs.filter(espEstado=estado)

        all_espacios = Espacio.objects.all()
        total = all_espacios.count()
        disponibles = all_espacios.filter(espEstado='DISPONIBLE').count()
        ocupados = all_espacios.filter(espEstado='OCUPADO').count()
        inactivos = all_espacios.filter(espEstado='INACTIVO').count()

        return render(request, 'admin_panel/espacios/list.html', {
            'active_page': 'espacios',
            'espacios': qs,
            'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
            'tipos': TipoEspacio.objects.order_by('nombre'),
            'q': q,
            'piso_sel': int(piso_id) if piso_id and piso_id.isdigit() else '',
            'tipo_sel': int(tipo_id) if tipo_id and tipo_id.isdigit() else '',
            'estado_sel': estado,
            'total': total,
            'disponibles': disponibles,
            'ocupados': ocupados,
            'inactivos': inactivos,
        })


class EspacioCreateView(AdminRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/espacios/form.html', {
            'active_page': 'espacios',
            'title': 'Nuevo Espacio',
            'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
            'tipos': TipoEspacio.objects.order_by('nombre'),
        })

    def post(self, request):
        numero = request.POST.get('espNumero', '').strip()
        piso_id = request.POST.get('fkIdPiso', '')
        tipo_id = request.POST.get('fkIdTipoEspacio', '')
        estado = request.POST.get('espEstado', 'DISPONIBLE')

        ctx = {
            'active_page': 'espacios',
            'title': 'Nuevo Espacio',
            'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
            'tipos': TipoEspacio.objects.order_by('nombre'),
            'espacio': {'espNumero': numero, 'fkIdPiso_id': piso_id, 'fkIdTipoEspacio_id': tipo_id, 'espEstado': estado},
        }

        if not all([numero, piso_id, tipo_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'admin_panel/espacios/form.html', ctx)

        Espacio.objects.create(
            espNumero=numero,
            fkIdPiso_id=piso_id,
            fkIdTipoEspacio_id=tipo_id,
            espEstado=estado,
        )
        messages.success(request, 'Espacio creado exitosamente.')
        return redirect('admin_espacios')


class EspacioUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        espacio = get_object_or_404(Espacio, pk=pk)
        return render(request, 'admin_panel/espacios/form.html', {
            'active_page': 'espacios',
            'title': 'Editar Espacio',
            'espacio': espacio,
            'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
            'tipos': TipoEspacio.objects.order_by('nombre'),
        })

    def post(self, request, pk):
        espacio = get_object_or_404(Espacio, pk=pk)
        espacio.espNumero = request.POST.get('espNumero', '').strip()
        espacio.fkIdPiso_id = request.POST.get('fkIdPiso', '')
        espacio.fkIdTipoEspacio_id = request.POST.get('fkIdTipoEspacio', '')
        espacio.espEstado = request.POST.get('espEstado', 'DISPONIBLE')

        if not all([espacio.espNumero, espacio.fkIdPiso_id, espacio.fkIdTipoEspacio_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'admin_panel/espacios/form.html', {
                'active_page': 'espacios',
                'title': 'Editar Espacio',
                'espacio': espacio,
                'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
                'tipos': TipoEspacio.objects.order_by('nombre'),
            })

        espacio.save()
        messages.success(request, 'Espacio actualizado.')
        return redirect('admin_espacios')


class EspacioDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        espacio = get_object_or_404(Espacio, pk=pk)
        if espacio.espEstado == 'OCUPADO':
            messages.error(request, 'No se puede eliminar un espacio ocupado.')
            return redirect('admin_espacios')
        espacio.delete()
        messages.success(request, 'Espacio eliminado.')
        return redirect('admin_espacios')


class EspacioRangeCreateView(AdminRequiredMixin, View):
    """Crear múltiples espacios por rango (ej: A-01 a A-20)."""
    def get(self, request):
        return render(request, 'admin_panel/espacios/range_form.html', {
            'active_page': 'espacios',
            'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
            'tipos': TipoEspacio.objects.order_by('nombre'),
        })

    def post(self, request):
        prefijo = request.POST.get('prefijo', '').strip()
        inicio = request.POST.get('inicio', '')
        fin = request.POST.get('fin', '')
        piso_id = request.POST.get('fkIdPiso', '')
        tipo_id = request.POST.get('fkIdTipoEspacio', '')

        ctx = {
            'active_page': 'espacios',
            'pisos': Piso.objects.filter(pisEstado=True).order_by('pisNombre'),
            'tipos': TipoEspacio.objects.order_by('nombre'),
            'prefijo': prefijo,
            'inicio': inicio,
            'fin': fin,
            'piso_sel': int(piso_id) if piso_id and piso_id.isdigit() else '',
            'tipo_sel': int(tipo_id) if tipo_id and tipo_id.isdigit() else '',
        }

        if not all([prefijo, inicio, fin, piso_id, tipo_id]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'admin_panel/espacios/range_form.html', ctx)

        try:
            inicio_n = int(inicio)
            fin_n = int(fin)
        except ValueError:
            messages.error(request, 'Inicio y fin deben ser números.')
            return render(request, 'admin_panel/espacios/range_form.html', ctx)

        if inicio_n > fin_n:
            messages.error(request, 'El inicio debe ser menor o igual al fin.')
            return render(request, 'admin_panel/espacios/range_form.html', ctx)

        if fin_n - inicio_n + 1 > 100:
            messages.error(request, 'Máximo 100 espacios por rango.')
            return render(request, 'admin_panel/espacios/range_form.html', ctx)

        creados = 0
        for i in range(inicio_n, fin_n + 1):
            numero = f'{prefijo}{i:02d}'
            if not Espacio.objects.filter(espNumero=numero, fkIdPiso_id=piso_id).exists():
                Espacio.objects.create(
                    espNumero=numero,
                    fkIdPiso_id=piso_id,
                    fkIdTipoEspacio_id=tipo_id,
                    espEstado='DISPONIBLE',
                )
                creados += 1

        messages.success(request, f'{creados} espacios creados exitosamente.')
        return redirect('admin_espacios')

# ── Ingreso Rápido (Visitantes/Usuarios) ─────────────────────────
class RegistrarIngresoView(AdminRequiredMixin, View):
    def post(self, request):
        placa = request.POST.get('placa', '').upper().strip()
        espacio_id = request.POST.get('espacio_id')
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        if not placa or not espacio_id:
            messages.error(request, 'Placa y Espacio son obligatorios.')
            return redirect('admin_dashboard')

        # 1. Validar Espacio
        espacio = get_object_or_404(Espacio, pk=espacio_id)
        if espacio.espEstado != 'DISPONIBLE':
            messages.error(request, f'El espacio {espacio.espNumero} no está disponible.')
            return redirect('admin_dashboard')

        # 2. Buscar/Crear Vehículo
        vehiculo = Vehiculo.objects.filter(vehPlaca=placa).first()
        if not vehiculo:
            # Crear como visitante
            vehiculo = Vehiculo.objects.create(
                vehPlaca=placa,
                vehTipo='Vehículo', # Tipo por defecto
                es_visitante=True,
                nombre_contacto=nombre,
                telefono_contacto=telefono
            )
        else:
            # Actualizar datos de contacto si se proporcionan y es visitante
            if vehiculo.es_visitante and (nombre or telefono):
                if nombre: vehiculo.nombre_contacto = nombre
                if telefono: vehiculo.telefono_contacto = telefono
                vehiculo.save()

        # 3. Verificar si ya tiene un ingreso activo (doble check)
        if InventarioParqueo.objects.filter(fkIdVehiculo=vehiculo, parHoraSalida__isnull=True).exists():
             messages.error(request, f'El vehículo {placa} ya tiene un ingreso activo.')
             return redirect('admin_dashboard')

        # 4. Registrar Ingreso
        InventarioParqueo.objects.create(
            fkIdVehiculo=vehiculo,
            fkIdEspacio=espacio
        )
        
        # 5. Actualizar Estado del Espacio
        espacio.espEstado = 'OCUPADO'
        espacio.save()

        messages.success(request, f'Ingreso registrado para {placa} en {espacio.espNumero}.')
        return redirect('admin_dashboard')


class BuscarVehiculoView(AdminRequiredMixin, View):
    def get(self, request):
        placa = request.GET.get('placa', '').upper().strip()
        if not placa:
            return JsonResponse({'error': 'Placa requerida'}, status=400)
        
        vehiculo = Vehiculo.objects.filter(vehPlaca=placa).first()
        if vehiculo:
            return JsonResponse({
                'found': True,
                'es_visitante': vehiculo.es_visitante,
                'nombre': vehiculo.nombre_contacto or (vehiculo.fkIdUsuario.usuNombreCompleto if vehiculo.fkIdUsuario else ""),
                'telefono': vehiculo.telefono_contacto or (vehiculo.fkIdUsuario.usuTelefono if vehiculo.fkIdUsuario else ""),
            })
        return JsonResponse({'found': False})


import math

class ObtenerDetalleOcupacionView(AdminRequiredMixin, View):
    def get(self, request):
        espacio_id = request.GET.get('espacio_id')
        if not espacio_id:
            return JsonResponse({'error': 'ID de espacio requerido'}, status=400)
        
        espacio = get_object_or_404(Espacio, pk=espacio_id)
        registro = InventarioParqueo.objects.filter(
            fkIdEspacio=espacio,
            parHoraSalida__isnull=True
        ).first()

        if registro:
            ahora = timezone.now()
            entrada = registro.parHoraEntrada
            duracion = ahora - entrada
            
            # Cálculo de Duración
            dias = duracion.days
            segundos = duracion.seconds
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            
            duracion_str = ""
            if dias > 0:
                duracion_str += f"{dias}d "
            if horas > 0:
                duracion_str += f"{horas}h "
            duracion_str += f"{minutos}m"
            if not duracion_str: 
                duracion_str = "Menos de 1m"

            # Cálculo de Costo (Tarifa por Hora)
            # Buscar tarifa activa para el tipo de espacio
            tarifa = Tarifa.objects.filter(
                fkIdTipoEspacio=espacio.fkIdTipoEspacio,
                activa=True
            ).first()

            total_pagar = 0
            tarifa_info = "Sin tarifa configurada"

            if tarifa:
                # Cobro por hora o fracción (redondeo hacia arriba)
                horas_totales = dias * 24 + horas + (1 if minutos > 0 else 0)
                if horas_totales == 0 and dias == 0: horas_totales = 1 # Mínimo 1 hora
                
                total_pagar = float(tarifa.precioHora) * horas_totales
                tarifa_info = f"${tarifa.precioHora:,.0f} / Hora"

            return JsonResponse({
                'found': True,
                'placa': registro.fkIdVehiculo.vehPlaca,
                'entrada': timezone.localtime(entrada).strftime('%d/%m/%Y %H:%M'),
                'duracion': duracion_str,
                'cliente': registro.fkIdVehiculo.fkIdUsuario.usuNombreCompleto if registro.fkIdVehiculo.fkIdUsuario else (registro.fkIdVehiculo.nombre_contacto or "Visitante"),
                'tipo_cliente': 'USUARIO' if registro.fkIdVehiculo.fkIdUsuario else 'VISITANTE',
                'telefono': registro.fkIdVehiculo.fkIdUsuario.usuTelefono if registro.fkIdVehiculo.fkIdUsuario else (registro.fkIdVehiculo.telefono_contacto or "Sin teléfono"),
                'tarifa_info': tarifa_info,
                'total_pagar': f"${total_pagar:,.0f}"
            })
        
        return JsonResponse({'found': False, 'error': 'No hay registro activo'})


class RegistrarSalidaView(AdminRequiredMixin, View):
    def post(self, request):
        espacio_id = request.POST.get('espacio_id')
        
        # 1. Validar Espacio y Ocupación
        espacio = get_object_or_404(Espacio, pk=espacio_id)
        if espacio.espEstado != 'OCUPADO':
            messages.error(request, f'El espacio {espacio.espNumero} no está ocupado.')
            return redirect('admin_dashboard')

        # 2. Buscar Registro Activo
        registro = InventarioParqueo.objects.filter(
            fkIdEspacio=espacio,
            parHoraSalida__isnull=True
        ).first()

        if not registro:
            espacio.espEstado = 'DISPONIBLE'
            espacio.save()
            messages.warning(request, f'Espacio {espacio.espNumero} liberado (no se encontró registro activo).')
            return redirect('admin_dashboard')

        # 3. Calcular Costo Final y Registrar Pago
        ahora = timezone.now()
        registro.parHoraSalida = ahora
        registro.save()
        
        # Lógica de Pago
        tarifa = Tarifa.objects.filter(
            fkIdTipoEspacio=espacio.fkIdTipoEspacio,
            activa=True
        ).first()
        
        monto_pagado = 0
        
        if tarifa:
            duracion = ahora - registro.parHoraEntrada
            dias = duracion.days
            segundos = duracion.seconds
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            
            horas_totales = dias * 24 + horas + (1 if minutos > 0 else 0)
            if horas_totales == 0 and dias == 0: horas_totales = 1
            
            monto_pagado = tarifa.precioHora * horas_totales

            # Crear registro de Pago
            Pago.objects.create(
                pagMonto=monto_pagado,
                pagMetodo='EFECTIVO', # Default por ahora
                pagEstado='PAGADO',
                fkIdParqueo=registro
            )

        # 4. Actualizar Espacio
        espacio.espEstado = 'DISPONIBLE'
        espacio.save()

        msg_pago = f" Pago registrado: ${monto_pagado:,.0f}" if monto_pagado > 0 else ""
        messages.success(request, f'Salida registrada para {registro.fkIdVehiculo.vehPlaca}.{msg_pago}')
        return redirect('admin_dashboard')
