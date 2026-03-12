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

    class Meta:
        db_table = 'reservas'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.pk} - {self.fkIdVehiculo.vehPlaca} ({self.resEstado})'
