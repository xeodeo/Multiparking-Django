from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import JsonResponse

from usuarios.mixins import AdminRequiredMixin

from .models import Reserva


class ReservaListView(AdminRequiredMixin, View):
    def get(self, request):
        reservas = Reserva.objects.select_related(
            'fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso'
        )

        # Filtro de búsqueda
        q = request.GET.get('q', '').strip()
        if q:
            reservas = reservas.filter(
                fkIdVehiculo__vehPlaca__icontains=q
            ) | reservas.filter(
                fkIdEspacio__espNumero__icontains=q
            )

        # Filtro de estado
        estado = request.GET.get('estado', '')
        if estado:
            reservas = reservas.filter(resEstado=estado)

        reservas = reservas.order_by('-resFechaReserva', '-resHoraInicio')

        total = reservas.count()

        return render(request, 'admin_panel/reservas/list.html', {
            'active_page': 'reservas',
            'reservas': reservas,
            'total': total,
            'q': q,
            'estado_sel': estado,
        })


class ReservaFinalizarView(AdminRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.resEstado in ('PENDIENTE', 'CONFIRMADA'):
            reserva.resEstado = 'COMPLETADA'
            reserva.save()
            messages.success(request, f'Reserva #{reserva.pk} finalizada.')
        else:
            messages.error(request, 'Esta reserva no se puede finalizar.')
        return redirect('admin_reservas')


class ReservaCancelarView(AdminRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.resEstado in ('PENDIENTE', 'CONFIRMADA'):
            reserva.resEstado = 'CANCELADA'
            reserva.save()
            # Liberar espacio si estaba reservado
            espacio = reserva.fkIdEspacio
            if espacio.espEstado == 'RESERVADO':
                espacio.espEstado = 'DISPONIBLE'
                espacio.save()
            messages.success(request, f'Reserva #{reserva.pk} cancelada.')
        else:
            messages.error(request, 'Esta reserva no se puede cancelar.')
        return redirect('admin_reservas')


class ReservaDetallesAPIView(View):
    """API endpoint para obtener detalles de una reserva"""
    def get(self, request, pk):
        try:
            reserva = Reserva.objects.select_related(
                'fkIdVehiculo__fkIdUsuario',
                'fkIdEspacio__fkIdPiso'
            ).get(pk=pk)

            data = {
                'placa': reserva.fkIdVehiculo.vehPlaca,
                'cliente': reserva.fkIdVehiculo.fkIdUsuario.usuNombreCompleto if reserva.fkIdVehiculo.fkIdUsuario else 'Visitante',
                'fecha': reserva.resFechaReserva.strftime('%Y-%m-%d'),
                'hora_inicio': reserva.resHoraInicio.strftime('%H:%M'),
                'hora_fin': reserva.resHoraFin.strftime('%H:%M'),
                'estado': reserva.get_resEstado_display(),
                'confirmada': reserva.resConfirmada,
            }
            return JsonResponse(data)
        except Reserva.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
