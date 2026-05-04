from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from decimal import Decimal

from usuarios.mixins import AdminRequiredMixin, _no_cache
from pagos.models import Pago


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
        ).prefetch_related('cupones_aplicados').order_by('-pagFechaPago')

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
        paginator = Paginator(pagos_qs, 20)
        page_obj = paginator.get_page(request.GET.get('page'))

        pagos_list = []
        for pago in page_obj:
            descuento_total = sum(
                ca.montoDescontado for ca in pago.cupones_aplicados.all()
            ) or Decimal('0')

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
            'page_obj': page_obj,
            'total_recaudado': total_recaudado,
            'pagos_realizados': pagos_realizados,
            'pagos_pendientes': pagos_pendientes,
            'search_query': search_query,
            'estado_filter': estado_filter,
            'estados': Pago.EstadoChoices.choices,
        }

        return render(request, 'admin_panel/pagos_list.html', context)


class ReciboView(View):
    def get(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('home')

        rol = request.session.get('usuario_rol')
        pago = get_object_or_404(
            Pago.objects.select_related(
                'fkIdParqueo__fkIdVehiculo__fkIdUsuario',
                'fkIdParqueo__fkIdEspacio__fkIdPiso',
            ).prefetch_related('cupones_aplicados__fkIdCupon'),
            pk=pk
        )

        # Clientes solo pueden ver sus propios recibos
        if rol == 'CLIENTE':
            vehiculo = pago.fkIdParqueo.fkIdVehiculo
            if not vehiculo.fkIdUsuario or vehiculo.fkIdUsuario_id != usuario_id:
                return redirect('dashboard')

        parqueo = pago.fkIdParqueo
        duracion_str = ''
        if parqueo.parHoraSalida and parqueo.parHoraEntrada:
            segundos = int((parqueo.parHoraSalida - parqueo.parHoraEntrada).total_seconds())
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            duracion_str = f"{horas}h {minutos}m" if horas > 0 else f"{minutos}m"

        cupones = pago.cupones_aplicados.all()
        descuento_total = sum(ca.montoDescontado for ca in cupones) or Decimal('0')
        monto_original = pago.pagMonto + descuento_total

        if rol == 'ADMIN':
            back_url = '/admin-panel/pagos/'
        elif rol == 'VIGILANTE':
            back_url = '/guardia/'
        else:
            back_url = '/dashboard/'

        return _no_cache(render(request, 'recibo/recibo.html', {
            'pago': pago,
            'parqueo': parqueo,
            'duracion': duracion_str,
            'cupones': cupones,
            'descuento_total': descuento_total,
            'monto_original': monto_original,
            'back_url': back_url,
        }))
