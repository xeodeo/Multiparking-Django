from django.db import models


class Reserva(models.Model):

    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        CANCELADA = 'CANCELADA', 'Cancelada'
        COMPLETADA = 'COMPLETADA', 'Completada'

    resFechaReserva = models.DateField()
    resHoraInicio = models.TimeField()
    resHoraFin = models.TimeField()
    resEstado = models.CharField(
        max_length=11,
        choices=EstadoChoices.choices,
        default=EstadoChoices.PENDIENTE,
    )
    resConfirmada = models.BooleanField(default=False)
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

    class Meta:
        db_table = 'reservas'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.pk} - {self.fkIdVehiculo.vehPlaca} ({self.resEstado})'
