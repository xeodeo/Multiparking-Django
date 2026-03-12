from django.db import models


class Pago(models.Model):

    class MetodoChoices(models.TextChoices):
        EFECTIVO = 'EFECTIVO', 'Efectivo'
        TARJETA = 'TARJETA', 'Tarjeta'
        TRANSFERENCIA = 'TRANSFERENCIA', 'Transferencia'
        PSE = 'PSE', 'PSE'

    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'    # Cobro en efectivo generado pero aún no confirmado por el vigilante
        PAGADO = 'PAGADO', 'Pagado'              # Pago confirmado
        ANULADO = 'ANULADO', 'Anulado'           # Pago cancelado

    pagFechaPago = models.DateTimeField(auto_now_add=True)  # Se asigna automáticamente al crear el registro
    pagMonto = models.DecimalField(max_digits=12, decimal_places=2)
    pagMetodo = models.CharField(
        max_length=13,
        choices=MetodoChoices.choices,
        default=MetodoChoices.EFECTIVO,
    )
    pagEstado = models.CharField(
        max_length=9,
        choices=EstadoChoices.choices,
        default=EstadoChoices.PENDIENTE,
    )
    fkIdParqueo = models.ForeignKey(
        'parqueadero.InventarioParqueo',
        on_delete=models.CASCADE,
        related_name='pagos',
        db_column='fkIdParqueo',
    )

    class Meta:
        db_table = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f'Pago {self.pk} - ${self.pagMonto} ({self.pagEstado})'
