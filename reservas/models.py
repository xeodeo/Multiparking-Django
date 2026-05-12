from django.db import models


class Reserva(models.Model):

    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'      # Creada pero no confirmada
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'   # Confirmada — aparece en el panel del vigilante como solicitud de entrada
        CANCELADA = 'CANCELADA', 'Cancelada'      # Cancelada por el usuario o admin
        COMPLETADA = 'COMPLETADA', 'Completada'   # El vehículo ya entró y salió

    resFechaReserva = models.DateField()
    resHoraInicio = models.TimeField()
    resHoraFin = models.TimeField(null=True, blank=True)  # Ahora es opcional
    resEstado = models.CharField(
        max_length=10,
        choices=EstadoChoices.choices,
        default=EstadoChoices.PENDIENTE,
    )
    fkIdEspacio = models.ForeignKey(
        'parqueadero.Espacio',
        on_delete=models.CASCADE,
        related_name='reservas',
        db_column='fkIdEspacio',
    )
    fkIdVehiculo = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.CASCADE,
        related_name='reservas',
        db_column='fkIdVehiculo',
    )

    @property
    def resConfirmada(self):
        # Propiedad calculada — NO es columna de BD
        # Shortcut para verificar si la reserva está en estado CONFIRMADA
        return self.resEstado == self.EstadoChoices.CONFIRMADA

    def cerrar(self, nuevo_estado):
        """Cambia el estado de la reserva y libera el espacio si estaba RESERVADO."""
        self.resEstado = nuevo_estado
        self.save()
        espacio = self.fkIdEspacio
        if espacio.espEstado == 'RESERVADO':
            espacio.liberar()

    @classmethod
    def cancelar_vencidas(cls):
        """
        Cancela las reservas PENDIENTES cuya hora de inicio ya pasó o está en ≤15 min,
        y libera los espacios que estaban bloqueados por ellas.
        """
        from django.utils import timezone
        from datetime import datetime, timedelta
        from parqueadero.models import Espacio
        now = timezone.now()
        ids_vencidas = [
            r.pk for r in cls.objects.filter(resEstado='PENDIENTE').select_related('fkIdEspacio')
            if (timezone.make_aware(datetime.combine(r.resFechaReserva, r.resHoraInicio)) - now)
               <= timedelta(minutes=15)
        ]
        if ids_vencidas:
            # Liberar los espacios antes de cancelar las reservas
            Espacio.objects.filter(
                reservas__pk__in=ids_vencidas,
                espEstado='RESERVADO'
            ).update(espEstado='DISPONIBLE')
            cls.objects.filter(pk__in=ids_vencidas).update(resEstado='CANCELADA')

    class Meta:
        db_table = 'reservas'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.pk} - {self.fkIdVehiculo.vehPlaca} ({self.resEstado})'
