from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from usuarios.mixins import AdminRequiredMixin
from pagos.models import Pago
from cupones.models import CuponAplicado


class PagosListView(AdminRequiredMixin, View):
    """
    Vista para listar pagos con estadísticas, búsqueda y filtros.
    """

    def get(self, request):
        # Parámetros de búsqueda y filtro
        search_query = request.GET.get('search', '').strip()
        estado_filter = request.GET.get('estado', 'TODOS')

        # Query base
        pagos_qs = Pago.objects.select_related(
            'fkIdParqueo',
            'fkIdParqueo__fkIdVehiculo',
            'fkIdParqueo__fkIdEspacio'
        ).order_by('-pagFechaPago')

        # Filtro por estado
        if estado_filter != 'TODOS':
            pagos_qs = pagos_qs.filter(pagEstado=estado_filter)

        # Búsqueda por ID de pago, placa, ID de inventario
        if search_query:
            pagos_qs = pagos_qs.filter(
                Q(pk__icontains=search_query) |
                Q(fkIdParqueo__fkIdVehiculo__vehPlaca__icontains=search_query) |
                Q(fkIdParqueo__pk__icontains=search_query)
            )

        # Calcular estadísticas globales (sin filtros de búsqueda, pero sí de estado)
        stats_qs = Pago.objects.all()
        if estado_filter != 'TODOS':
            stats_qs = stats_qs.filter(pagEstado=estado_filter)

        # Total recaudado (solo pagos PAGADO)
        total_recaudado = Pago.objects.filter(
            pagEstado=Pago.EstadoChoices.PAGADO
        ).aggregate(
            total=Sum('pagMonto')
        )['total'] or Decimal('0')

        # Pagos realizados
        pagos_realizados = Pago.objects.filter(
            pagEstado=Pago.EstadoChoices.PAGADO
        ).count()

        # Pagos pendientes
        pagos_pendientes = Pago.objects.filter(
            pagEstado=Pago.EstadoChoices.PENDIENTE
        ).count()

        # Procesar cada pago para agregar descuento
        pagos_list = []
        for pago in pagos_qs:
            # Calcular descuento total aplicado
            descuento_total = CuponAplicado.objects.filter(
                fkIdPago=pago
            ).aggregate(
                total=Sum('montoDescontado')
            )['total'] or Decimal('0')

            pagos_list.append({
                'id': f'pay{pago.pk}',
                'pago': pago,
                'registro': f'inv{pago.fkIdParqueo.pk}',
                'placa': pago.fkIdParqueo.fkIdVehiculo.vehPlaca,
                'descuento': descuento_total,
                'total': pago.pagMonto,
            })

        context = {
            'active_page': 'pagos',
            'pagos': pagos_list,
            'total_recaudado': total_recaudado,
            'pagos_realizados': pagos_realizados,
            'pagos_pendientes': pagos_pendientes,
            'search_query': search_query,
            'estado_filter': estado_filter,
            'estados': Pago.EstadoChoices.choices,
        }

        return render(request, 'admin_panel/pagos_list.html', context)
