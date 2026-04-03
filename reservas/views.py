from datetime import datetime, date, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse

from usuarios.mixins import AdminRequiredMixin
from parqueadero.models import Espacio
from vehiculos.models import Vehiculo

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
        page_obj = Paginator(reservas, 20).get_page(request.GET.get('page'))

        return render(request, 'admin_panel/reservas/list.html', {
            'active_page': 'reservas',
            'reservas': page_obj,
            'page_obj': page_obj,
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
            espacio = reserva.fkIdEspacio
            if espacio.espEstado == 'RESERVADO':
                espacio.espEstado = 'DISPONIBLE'
                espacio.save()
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
            # Si el espacio estaba en estado RESERVADO, lo libera al cancelar
            espacio = reserva.fkIdEspacio
            if espacio.espEstado == 'RESERVADO':
                espacio.espEstado = 'DISPONIBLE'
                espacio.save()
            messages.success(request, f'Reserva #{reserva.pk} cancelada.')
        else:
            messages.error(request, 'Esta reserva no se puede cancelar.')
        return redirect('admin_reservas')


class ReservaEditarView(AdminRequiredMixin, View):
    def get(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk, resEstado__in=['PENDIENTE', 'CONFIRMADA'])
        espacios = Espacio.objects.filter(espEstado__in=['DISPONIBLE', 'RESERVADO']).select_related('fkIdPiso')
        vehiculos = Vehiculo.objects.filter(vehEstado=True).select_related('fkIdUsuario')
        return render(request, 'admin_panel/reservas/form.html', {
            'active_page': 'reservas',
            'reserva': reserva,
            'espacios': espacios,
            'vehiculos': vehiculos,
        })

    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk, resEstado__in=['PENDIENTE', 'CONFIRMADA'])

        espacio_id = request.POST.get('espacio_id')
        vehiculo_id = request.POST.get('vehiculo_id')
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')

        if not all([espacio_id, vehiculo_id, fecha, hora_inicio]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('admin_reservas_editar', pk=pk)

        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora_inicio, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Fecha u hora inválida.')
            return redirect('admin_reservas_editar', pk=pk)

        try:
            nuevo_espacio = Espacio.objects.get(pk=espacio_id)
        except Espacio.DoesNotExist:
            messages.error(request, 'Espacio no válido.')
            return redirect('admin_reservas_editar', pk=pk)

        try:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
        except Vehiculo.DoesNotExist:
            messages.error(request, 'Vehículo no válido.')
            return redirect('admin_reservas_editar', pk=pk)

        # Verificar conflicto de espacio en el mismo horario (excluyendo esta reserva)
        conflicto = Reserva.objects.filter(
            fkIdEspacio=nuevo_espacio,
            resFechaReserva=fecha_obj,
            resHoraInicio=hora_obj,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        ).exclude(pk=pk).exists()

        if conflicto:
            messages.error(request, 'El espacio ya está reservado en ese horario.')
            return redirect('admin_reservas_editar', pk=pk)

        # Si cambia el espacio, liberar el anterior y bloquear el nuevo
        espacio_anterior = reserva.fkIdEspacio
        if espacio_anterior.pk != nuevo_espacio.pk:
            if espacio_anterior.espEstado == 'RESERVADO':
                espacio_anterior.espEstado = 'DISPONIBLE'
                espacio_anterior.save()
            if nuevo_espacio.espEstado == 'DISPONIBLE':
                nuevo_espacio.espEstado = 'RESERVADO'
                nuevo_espacio.save()

        reserva.fkIdEspacio = nuevo_espacio
        reserva.fkIdVehiculo = vehiculo
        reserva.resFechaReserva = fecha_obj
        reserva.resHoraInicio = hora_obj
        reserva.save()

        messages.success(request, f'Reserva #{reserva.pk} actualizada.')
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
                'hora_inicio': reserva.resHoraInicio.strftime('%I:%M %p'),
                'hora_fin': reserva.resHoraFin.strftime('%I:%M %p') if reserva.resHoraFin else None,
                'estado': reserva.get_resEstado_display(),
                'confirmada': reserva.resConfirmada,
            }
            return JsonResponse(data)
        except Reserva.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada'}, status=404)
