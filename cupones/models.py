from django.db import models


class Cupon(models.Model):

    class TipoChoices(models.TextChoices):
        PORCENTAJE = 'PORCENTAJE', 'Porcentaje'
        VALOR_FIJO = 'VALOR_FIJO', 'Valor Fijo'

    cupNombre = models.CharField(max_length=100)
    cupTipo = models.CharField(
        max_length=10,
        choices=TipoChoices.choices,
    )
    cupValor = models.DecimalField(max_digits=10, decimal_places=2)
    cupDescripcion = models.TextField(blank=True)
    cupFechaInicio = models.DateField()
    cupFechaFin = models.DateField()
    cupActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cupones'
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'

    def __str__(self):
        return f'{self.cupNombre} ({self.cupTipo})'


class CuponAplicado(models.Model):
    fkIdPago = models.ForeignKey(
        'pagos.Pago',
        on_delete=models.CASCADE,
        related_name='cupones_aplicados',
        db_column='fkIdPago',
    )
    fkIdCupon = models.ForeignKey(
        Cupon,
        on_delete=models.CASCADE,
        related_name='aplicaciones',
        db_column='fkIdCupon',
    )
    montoDescontado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'cupones_aplicados'
        verbose_name = 'Cupón Aplicado'
        verbose_name_plural = 'Cupones Aplicados'

    def __str__(self):
        return f'Cupón {self.fkIdCupon.cupNombre} → Pago {self.fkIdPago.pk}'
