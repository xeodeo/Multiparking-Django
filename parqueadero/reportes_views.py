"""
Vistas para el módulo de Reportes y Estadísticas
"""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import json

from usuarios.mixins import AdminRequiredMixin
from parqueadero.models import Piso, Espacio, InventarioParqueo
from pagos.models import Pago
from reservas.models import Reserva


class ReportesView(AdminRequiredMixin, View):
    """
    Vista principal de Reportes y Estadísticas con gráficas interactivas
    """

    def get(self, request):
        # Filtros
        periodo = request.GET.get('periodo', 'mes')  # mes, semana, año
        piso_id = request.GET.get('piso', 'todos')

        # Fechas según período
        now = timezone.now()
        if periodo == 'semana':
            fecha_inicio = now - timedelta(days=7)
        elif periodo == 'mes':
            fecha_inicio = now - timedelta(days=30)
        elif periodo == 'año':
            fecha_inicio = now - timedelta(days=365)
        else:
            fecha_inicio = now - timedelta(days=30)

        # Query base de inventario parqueo
        inventario_qs = InventarioParqueo.objects.filter(
            parHoraEntrada__gte=fecha_inicio
        )

        # Filtro por piso
        if piso_id != 'todos':
            inventario_qs = inventario_qs.filter(
                fkIdEspacio__fkIdPiso__pk=int(piso_id)
            )

        # ══════════════════════════════════════════
        # 1. MÉTRICAS PRINCIPALES
        # ══════════════════════════════════════════

        # Total espacios
        total_espacios = Espacio.objects.filter(espEstado__in=['DISPONIBLE', 'OCUPADO']).count()

        # Espacios actualmente ocupados
        espacios_ocupados = Espacio.objects.filter(espEstado='OCUPADO').count()

        # Ocupación promedio en el período
        if total_espacios > 0:
            ocupacion_promedio = int((espacios_ocupados / total_espacios) * 100)
        else:
            ocupacion_promedio = 0

        # Variación vs mes anterior
        mes_anterior_inicio = fecha_inicio - timedelta(days=30)
        inventario_mes_anterior = InventarioParqueo.objects.filter(
            parHoraEntrada__gte=mes_anterior_inicio,
            parHoraEntrada__lt=fecha_inicio
        ).count()
        inventario_actual = inventario_qs.count()

        if inventario_mes_anterior > 0:
            variacion_ocupacion = int(((inventario_actual - inventario_mes_anterior) / inventario_mes_anterior) * 100)
        else:
            variacion_ocupacion = 0

        # Ingresos mensuales (suma de pagos)
        ingresos_totales = Pago.objects.filter(
            pagFechaPago__gte=fecha_inicio,
            pagEstado=Pago.EstadoChoices.PAGADO
        ).aggregate(
            total=Sum('pagMonto')
        )['total'] or Decimal('0')

        ingresos_mes_anterior = Pago.objects.filter(
            pagFechaPago__gte=mes_anterior_inicio,
            pagFechaPago__lt=fecha_inicio,
            pagEstado=Pago.EstadoChoices.PAGADO
        ).aggregate(
            total=Sum('pagMonto')
        )['total'] or Decimal('0')

        if ingresos_mes_anterior > 0:
            variacion_ingresos = int(((ingresos_totales - ingresos_mes_anterior) / ingresos_mes_anterior) * 100)
        else:
            variacion_ingresos = 0

        # Usuarios activos (vehículos diferentes que han ingresado)
        usuarios_activos = inventario_qs.values('fkIdVehiculo').distinct().count()

        usuarios_mes_anterior = InventarioParqueo.objects.filter(
            parHoraEntrada__gte=mes_anterior_inicio,
            parHoraEntrada__lt=fecha_inicio
        ).values('fkIdVehiculo').distinct().count()

        if usuarios_mes_anterior > 0:
            variacion_usuarios = int(((usuarios_activos - usuarios_mes_anterior) / usuarios_mes_anterior) * 100)
        else:
            variacion_usuarios = 0

        # Rotación diaria (promedio de entradas por espacio)
        dias_en_periodo = (now - fecha_inicio).days or 1
        rotacion_diaria = round(inventario_actual / total_espacios / dias_en_periodo, 1) if total_espacios > 0 else 0

        # ══════════════════════════════════════════
        # 2. TENDENCIA DE OCUPACIÓN DIARIA (por hora HOY)
        # ══════════════════════════════════════════

        # Obtener fecha local de hoy
        hoy_local = timezone.localtime(now).date()

        # Traer todos los registros del día actual
        registros_hoy = InventarioParqueo.objects.filter(
            parHoraEntrada__range=(
                timezone.make_aware(datetime.combine(hoy_local, datetime.min.time())),
                timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))
            )
        )

        # Contar por hora en Python (más eficiente)
        counts_por_hora = {h: 0 for h in range(6, 23)}
        for r in registros_hoy:
            h = timezone.localtime(r.parHoraEntrada).hour
            if 6 <= h < 23:
                counts_por_hora[h] += 1

        # Generar labels y data
        ocupacion_labels = []
        ocupacion_data = []
        for h in range(6, 23):
            ocupacion_labels.append(f"{h}:00")
            ocupacion_data.append(counts_por_hora[h])

        # ══════════════════════════════════════════
        # 3. INGRESOS MENSUALES (últimos 6 meses)
        # ══════════════════════════════════════════

        ingresos_labels = []
        ingresos_data_values = []

        for i in range(5, -1, -1):  # Últimos 6 meses
            mes_inicio = now - timedelta(days=30 * (i + 1))
            mes_fin = now - timedelta(days=30 * i)

            ingresos_mes = Pago.objects.filter(
                pagFechaPago__gte=mes_inicio,
                pagFechaPago__lt=mes_fin,
                pagEstado=Pago.EstadoChoices.PAGADO
            ).aggregate(
                total=Sum('pagMonto')
            )['total'] or Decimal('0')

            # Nombre del mes
            mes_nombre = mes_inicio.strftime('%b')
            ingresos_labels.append(mes_nombre)
            ingresos_data_values.append(float(ingresos_mes))

        # ══════════════════════════════════════════
        # 4. DISTRIBUCIÓN DE USO (Pie Chart)
        # ══════════════════════════════════════════

        # Residentes (vehículos registrados no visitantes)
        residentes_count = inventario_qs.filter(
            fkIdVehiculo__es_visitante=False
        ).count()

        # Visitantes
        visitantes_count = inventario_qs.filter(
            fkIdVehiculo__es_visitante=True
        ).count()

        # Reservas
        reservas_count = Reserva.objects.filter(
            resHoraInicio__gte=fecha_inicio
        ).count()

        total_uso = residentes_count + visitantes_count + reservas_count

        if total_uso > 0:
            residentes_pct = int((residentes_count / total_uso) * 100)
            visitantes_pct = int((visitantes_count / total_uso) * 100)
            reservas_pct = 100 - residentes_pct - visitantes_pct  # Resto para evitar errores de redondeo
        else:
            residentes_pct = visitantes_pct = reservas_pct = 0

        # ══════════════════════════════════════════
        # 5. RESUMEN POR PISO
        # ══════════════════════════════════════════

        pisos = Piso.objects.filter(pisEstado=True).prefetch_related('espacios')
        resumen_pisos = []

        for piso in pisos:
            total_espacios_piso = piso.espacios.filter(
                espEstado__in=['DISPONIBLE', 'OCUPADO']
            ).count()

            ocupados_piso = piso.espacios.filter(espEstado='OCUPADO').count()

            if total_espacios_piso > 0:
                ocupacion_piso = int((ocupados_piso / total_espacios_piso) * 100)
            else:
                ocupacion_piso = 0

            # Ingresos del piso
            ingresos_piso = Pago.objects.filter(
                fkIdParqueo__fkIdEspacio__fkIdPiso=piso,
                pagFechaPago__gte=fecha_inicio,
                pagEstado=Pago.EstadoChoices.PAGADO
            ).aggregate(
                total=Sum('pagMonto')
            )['total'] or Decimal('0')

            resumen_pisos.append({
                'nombre': piso.pisNombre,
                'ocupacion': ocupacion_piso,
                'ingresos': ingresos_piso,
            })

        # ══════════════════════════════════════════
        # CONTEXTO
        # ══════════════════════════════════════════

        context = {
            'active_page': 'reportes',
            # Filtros
            'periodo': periodo,
            'piso_id': piso_id,
            'pisos': pisos,

            # Métricas principales
            'ocupacion_promedio': ocupacion_promedio,
            'variacion_ocupacion': variacion_ocupacion,
            'ingresos_totales': ingresos_totales,
            'variacion_ingresos': variacion_ingresos,
            'usuarios_activos': usuarios_activos,
            'variacion_usuarios': variacion_usuarios,
            'rotacion_diaria': rotacion_diaria,

            # Datos para gráficas (convertidos a JSON)
            'ocupacion_labels': json.dumps(ocupacion_labels),
            'ocupacion_data': json.dumps(ocupacion_data),
            'ingresos_labels': json.dumps(ingresos_labels),
            'ingresos_data': json.dumps(ingresos_data_values),

            # Distribución de uso
            'residentes_pct': residentes_pct,
            'visitantes_pct': visitantes_pct,
            'reservas_pct': reservas_pct,

            # Resumen por piso
            'resumen_pisos': resumen_pisos,
        }

        return render(request, 'admin_panel/reportes.html', context)


class ExportarPDFReportesView(AdminRequiredMixin, View):
    """
    Exportar reportes a PDF
    """
    def get(self, request):
        # TODO: Implementar exportación PDF con ReportLab o WeasyPrint
        return HttpResponse("Exportación PDF en desarrollo", content_type="text/plain")


class ExportarExcelReportesView(AdminRequiredMixin, View):
    """
    Exportar reportes a Excel
    """
    def get(self, request):
        # TODO: Implementar exportación Excel con openpyxl
        return HttpResponse("Exportación Excel en desarrollo", content_type="text/plain")
