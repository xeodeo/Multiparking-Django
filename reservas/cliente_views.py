"""
Vistas para que los clientes creen y gestionen sus reservas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils import timezone
from datetime import datetime, date, timedelta

from usuarios.models import Usuario
from vehiculos.models import Vehiculo
from parqueadero.models import Espacio, Piso
from reservas.models import Reserva


class ClienteRequiredMixin:
    """Mixin para requerir que el usuario sea un cliente autenticado"""
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class ClienteCrearReservaView(ClienteRequiredMixin, View):
    """Vista para que un cliente cree una reserva"""

    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        # Obtener vehículos activos del usuario
        vehiculos = Vehiculo.objects.filter(
            fkIdUsuario=usuario,
            es_visitante=False,
            vehEstado=True
        )

        # Obtener todos los pisos
        pisos = Piso.objects.filter(pisEstado=True).prefetch_related('espacios')

        return render(request, 'cliente/reserva_form.html', {
            'title': 'Crear Reserva',
            'vehiculos': vehiculos,
            'pisos': pisos,
        })

    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        vehiculo_id = request.POST.get('vehiculo_id')
        espacio_id = request.POST.get('espacio_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        hora_inicio = request.POST.get('hora_inicio')

        # Validaciones
        if not all([vehiculo_id, espacio_id, fecha_inicio, hora_inicio]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return self.get(request)

        # Validar que el vehículo pertenezca al usuario
        try:
            vehiculo = Vehiculo.objects.get(
                pk=vehiculo_id,
                fkIdUsuario=usuario,
                es_visitante=False,
                vehEstado=True
            )
        except Vehiculo.DoesNotExist:
            messages.error(request, 'Vehículo no válido.')
            return self.get(request)

        # Validar que el espacio exista y esté disponible
        try:
            espacio = Espacio.objects.get(pk=espacio_id, espEstado='DISPONIBLE')
        except Espacio.DoesNotExist:
            messages.error(request, 'El espacio seleccionado no está disponible.')
            return self.get(request)

        # Validar que la fecha no sea en el pasado
        fecha_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        if fecha_obj < date.today():
            messages.error(request, 'No puedes reservar en fechas pasadas.')
            return self.get(request)

        # Parsear hora de inicio
        hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()

        # Validar que la hora de reserva sea mayor a la hora actual
        now = timezone.now()
        now_local = timezone.localtime(now)  # Convertir a hora local de Bogotá

        # Si es hoy, la hora debe ser mayor a la hora actual
        if fecha_obj == date.today():
            hora_actual = now_local.time().hour
            hora_reserva = hora_inicio_obj.hour

            if hora_reserva <= hora_actual:
                messages.error(request, f'No puedes reservar para la misma hora. La reserva debe ser para las {hora_actual + 1}:00 en adelante.')
                return self.get(request)

        # Validar que la reserva sea con al menos 1 hora de anticipación
        fecha_hora_inicio = timezone.make_aware(datetime.combine(fecha_obj, hora_inicio_obj))
        if fecha_hora_inicio - now < timedelta(hours=1):
            messages.error(request, 'Debes reservar con al menos 1 hora de anticipación.')
            return self.get(request)

        # Verificar que no haya otra reserva para el mismo espacio en la misma fecha y hora
        reservas_conflicto = Reserva.objects.filter(
            fkIdEspacio=espacio,
            resFechaReserva=fecha_inicio,
            resHoraInicio=hora_inicio_obj,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        )

        if reservas_conflicto.exists():
            messages.error(request, 'El espacio ya está reservado en ese horario.')
            return self.get(request)

        # Crear la reserva (sin hora de fin)
        Reserva.objects.create(
            resFechaReserva=fecha_inicio,
            resHoraInicio=hora_inicio_obj,
            resEstado='PENDIENTE',
            fkIdEspacio=espacio,
            fkIdVehiculo=vehiculo
        )

        messages.success(request, f'Reserva creada exitosamente para {vehiculo.vehPlaca} el {fecha_inicio} a las {hora_inicio}.')
        return redirect('dashboard')


class ClienteEditarReservaView(ClienteRequiredMixin, View):
    """Vista para que un cliente edite su reserva"""

    def get(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        # Obtener la reserva y verificar que pertenece al usuario
        reserva = get_object_or_404(
            Reserva,
            pk=pk,
            fkIdVehiculo__fkIdUsuario=usuario,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        )

        # Verificar que no esté muy cerca de la fecha de reserva (min 1h antes)
        now = timezone.now()
        fecha_hora_reserva = datetime.combine(reserva.resFechaReserva, reserva.resHoraInicio)
        fecha_hora_reserva = timezone.make_aware(fecha_hora_reserva)

        if fecha_hora_reserva - now < timedelta(hours=1):
            messages.error(request, 'No puedes editar una reserva con menos de 1 hora de anticipación.')
            return redirect('dashboard')

        # Obtener vehículos activos del usuario
        vehiculos = Vehiculo.objects.filter(
            fkIdUsuario=usuario,
            es_visitante=False,
            vehEstado=True
        )

        # Obtener todos los pisos
        pisos = Piso.objects.filter(pisEstado=True).prefetch_related('espacios')

        return render(request, 'cliente/reserva_form.html', {
            'title': 'Editar Reserva',
            'vehiculos': vehiculos,
            'pisos': pisos,
            'reserva': reserva,
        })

    def post(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        reserva = get_object_or_404(
            Reserva,
            pk=pk,
            fkIdVehiculo__fkIdUsuario=usuario,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        )

        vehiculo_id = request.POST.get('vehiculo_id')
        espacio_id = request.POST.get('espacio_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        hora_inicio = request.POST.get('hora_inicio')

        # Validaciones
        if not all([vehiculo_id, espacio_id, fecha_inicio, hora_inicio]):
            messages.error(request, 'Todos los campos son obligatorios.')
            return self.get(request, pk)

        # Validar que el vehículo pertenezca al usuario
        try:
            vehiculo = Vehiculo.objects.get(
                pk=vehiculo_id,
                fkIdUsuario=usuario,
                es_visitante=False,
                vehEstado=True
            )
        except Vehiculo.DoesNotExist:
            messages.error(request, 'Vehículo no válido.')
            return self.get(request, pk)

        # Validar que el espacio exista y esté disponible
        try:
            espacio = Espacio.objects.get(pk=espacio_id, espEstado='DISPONIBLE')
        except Espacio.DoesNotExist:
            messages.error(request, 'El espacio seleccionado no está disponible.')
            return self.get(request, pk)

        # Validar que la fecha no sea en el pasado
        fecha_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        if fecha_obj < date.today():
            messages.error(request, 'No puedes reservar en fechas pasadas.')
            return self.get(request, pk)

        # Parsear hora de inicio
        hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()

        # Validar que la hora de reserva sea mayor a la hora actual
        now = timezone.now()
        now_local = timezone.localtime(now)  # Convertir a hora local de Bogotá

        # Si es hoy, la hora debe ser mayor a la hora actual
        if fecha_obj == date.today():
            hora_actual = now_local.time().hour
            hora_reserva = hora_inicio_obj.hour

            if hora_reserva <= hora_actual:
                messages.error(request, f'No puedes reservar para la misma hora. La reserva debe ser para las {hora_actual + 1}:00 en adelante.')
                return self.get(request, pk)

        # Validar que la reserva sea con al menos 1 hora de anticipación
        fecha_hora_inicio = timezone.make_aware(datetime.combine(fecha_obj, hora_inicio_obj))
        if fecha_hora_inicio - now < timedelta(hours=1):
            messages.error(request, 'Debes reservar con al menos 1 hora de anticipación.')
            return self.get(request, pk)

        # Verificar que no haya otra reserva para el mismo espacio en la misma fecha y hora (excluyendo esta reserva)
        reservas_conflicto = Reserva.objects.filter(
            fkIdEspacio=espacio,
            resFechaReserva=fecha_inicio,
            resHoraInicio=hora_inicio_obj,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        ).exclude(pk=pk)

        if reservas_conflicto.exists():
            messages.error(request, 'El espacio ya está reservado en ese horario.')
            return self.get(request, pk)

        # Actualizar la reserva (sin hora de fin)
        reserva.fkIdVehiculo = vehiculo
        reserva.fkIdEspacio = espacio
        reserva.resFechaReserva = fecha_inicio
        reserva.resHoraInicio = hora_inicio_obj
        reserva.save()

        messages.success(request, f'Reserva actualizada exitosamente.')
        return redirect('dashboard')


class ClienteCancelarReservaView(ClienteRequiredMixin, View):
    """Vista para que un cliente cancele su reserva"""

    def post(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        reserva = get_object_or_404(
            Reserva,
            pk=pk,
            fkIdVehiculo__fkIdUsuario=usuario,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        )

        # Cancelar la reserva (permitido en cualquier momento)
        reserva.resEstado = 'CANCELADA'
        reserva.save()

        messages.success(request, f'Reserva cancelada exitosamente.')
        return redirect('dashboard')


class ClienteConfirmarReservaView(ClienteRequiredMixin, View):
    """Vista para que un cliente confirme su reserva cuando falte menos de 1h"""

    def post(self, request, pk):
        usuario_id = request.session.get('usuario_id')
        usuario = Usuario.objects.get(pk=usuario_id)

        reserva = get_object_or_404(
            Reserva,
            pk=pk,
            fkIdVehiculo__fkIdUsuario=usuario,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        )

        # Marcar como confirmada
        reserva.resConfirmada = True
        reserva.resEstado = 'CONFIRMADA'
        reserva.save()

        messages.success(request, f'Reserva confirmada. Te esperamos en el parqueadero.')
        return redirect('dashboard')
