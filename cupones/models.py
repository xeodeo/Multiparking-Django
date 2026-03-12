from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Cupon(models.Model):

    class TipoChoices(models.TextChoices):
        PORCENTAJE = 'PORCENTAJE', 'Porcentaje'  # Descuento como % del total (ej. 20%)
        VALOR_FIJO = 'VALOR_FIJO', 'Valor Fijo'  # Descuento como monto fijo en COP (ej. $5,000)

    cupNombre = models.CharField(max_length=50)
    cupCodigo = models.CharField(
        max_length=20, unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'El código solo acepta letras mayúsculas y números')],
    )
    cupTipo = models.CharField(
        max_length=10,
        choices=TipoChoices.choices,
    )
    cupValor = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0, 'El valor no puede ser negativo')],
    )
    cupDescripcion = models.TextField(blank=True)
    cupFechaInicio = models.DateField()
    cupFechaFin = models.DateField()         # Las vistas validan que la fecha actual esté dentro del rango antes de aplicar
    cupActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cupones'
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'

    def __str__(self):
        return f'{self.cupNombre} ({self.cupTipo})'


class CuponAplicado(models.Model):
    # Tabla pivote que registra qué cupón fue aplicado a qué pago y cuánto se descontó efectivamente
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
    montoDescontado = models.DecimalField(max_digits=10, decimal_places=2)  # Monto real descontado al momento del pago

    class Meta:
        db_table = 'cupones_aplicados'
        verbose_name = 'Cupón Aplicado'
        verbose_name_plural = 'Cupones Aplicados'
        unique_together = [('fkIdPago', 'fkIdCupon')]  # Un cupón no puede aplicarse dos veces al mismo pago

    def __str__(self):
        return f'Cupón {self.fkIdCupon.cupNombre} → Pago {self.fkIdPago.pk}'
