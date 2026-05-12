from datetime import datetime, date, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.http import JsonResponse

from usuarios.mixins import AdminRequiredMixin, VigilanteRequiredMixin
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
            with transaction.atomic():
                reserva.cerrar('COMPLETADA')
            messages.success(request, f'Reserva #{reserva.pk} finalizada.')
        else:
            messages.error(request, 'Esta reserva no se puede finalizar.')
        return redirect('admin_reservas')


class ReservaCancelarView(AdminRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        if reserva.resEstado in ('PENDIENTE', 'CONFIRMADA'):
            with transaction.atomic():
                reserva.cerrar('CANCELADA')
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

        with transaction.atomic():
            # Si cambia el espacio, liberar el anterior y bloquear el nuevo
            espacio_anterior = reserva.fkIdEspacio
            if espacio_anterior.pk != nuevo_espacio.pk:
                if espacio_anterior.espEstado == 'RESERVADO':
                    espacio_anterior.liberar()
                if nuevo_espacio.espEstado == 'DISPONIBLE':
                    nuevo_espacio.reservar()

            reserva.fkIdEspacio = nuevo_espacio
            reserva.fkIdVehiculo = vehiculo
            reserva.resFechaReserva = fecha_obj
            reserva.resHoraInicio = hora_obj
            reserva.save()

        messages.success(request, f'Reserva #{reserva.pk} actualizada.')
        return redirect('admin_reservas')


class AdminCrearReservaView(AdminRequiredMixin, View):
    """Admin crea una reserva desde el mapa de espacios del dashboard."""

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        espacio_id = request.POST.get('espacio_id')
        vehiculo_id = request.POST.get('vehiculo_id')
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin') or None

        if not all([espacio_id, vehiculo_id, fecha, hora_inicio]):
            msg = 'Todos los campos son obligatorios.'
            if is_ajax:
                return JsonResponse({'ok': False, 'error': msg}, status=400)
            messages.error(request, msg)
            return redirect('admin_dashboard')

        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
            hora_fin_obj = datetime.strptime(hora_fin, '%H:%M').time() if hora_fin else None
        except ValueError:
            msg = 'Fecha u hora inválida.'
            if is_ajax:
                return JsonResponse({'ok': False, 'error': msg}, status=400)
            messages.error(request, msg)
            return redirect('admin_dashboard')

        try:
            espacio = Espacio.objects.get(pk=espacio_id, espEstado='DISPONIBLE')
        except Espacio.DoesNotExist:
            msg = 'El espacio no está disponible.'
            if is_ajax:
                return JsonResponse({'ok': False, 'error': msg}, status=400)
            messages.error(request, msg)
            return redirect('admin_dashboard')

        try:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
        except Vehiculo.DoesNotExist:
            msg = 'Vehículo no válido.'
            if is_ajax:
                return JsonResponse({'ok': False, 'error': msg}, status=400)
            messages.error(request, msg)
            return redirect('admin_dashboard')

        conflicto = Reserva.objects.filter(
            fkIdEspacio=espacio,
            resFechaReserva=fecha_obj,
            resHoraInicio=hora_inicio_obj,
            resEstado__in=['PENDIENTE', 'CONFIRMADA'],
        ).exists()

        if conflicto:
            msg = 'El espacio ya tiene una reserva en ese horario.'
            if is_ajax:
                return JsonResponse({'ok': False, 'error': msg}, status=400)
            messages.error(request, msg)
            return redirect('admin_dashboard')

        with transaction.atomic():
            reserva = Reserva.objects.create(
                fkIdEspacio=espacio,
                fkIdVehiculo=vehiculo,
                resFechaReserva=fecha_obj,
                resHoraInicio=hora_inicio_obj,
                resHoraFin=hora_fin_obj,
                resEstado='PENDIENTE',
            )
            espacio.reservar()

        if is_ajax:
            return JsonResponse({'ok': True, 'reserva_id': reserva.pk})
        messages.success(request, f'Reserva #{reserva.pk} creada para {vehiculo.vehPlaca}.')
        return redirect('admin_dashboard')


class AdminClientesVehiculosAPIView(AdminRequiredMixin, View):
    """Devuelve clientes activos y sus vehículos para el modal de reserva."""

    def get(self, request):
        from usuarios.models import Usuario
        clientes = Usuario.objects.filter(
            rolTipoRol='CLIENTE', usuEstado=True
        ).order_by('usuNombre', 'usuApellido')

        vehiculos = Vehiculo.objects.filter(
            fkIdUsuario__isnull=False,
            fkIdUsuario__usuEstado=True,
        ).select_related('fkIdUsuario').order_by('vehPlaca')

        return JsonResponse({
            'clientes': [
                {'id': u.pk, 'nombre': u.usuNombreCompleto}
                for u in clientes
            ],
            'vehiculos': [
                {'id': v.pk, 'placa': v.vehPlaca, 'usuario_id': v.fkIdUsuario.pk}
                for v in vehiculos
            ],
        })


class ReservaDetallesAPIView(VigilanteRequiredMixin, View):
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
