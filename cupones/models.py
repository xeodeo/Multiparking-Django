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

    def calcular_descuento(self, monto):
        """
        Calcula el monto a descontar según el tipo del cupón.
        Centraliza la lógica PORCENTAJE/VALOR_FIJO para evitar if/elif en vistas.

        - PORCENTAJE: aplica el % sobre el monto total.
        - VALOR_FIJO: descuenta el valor fijo, sin exceder el monto total.
        Retorna Decimal.
        """
        from decimal import Decimal
        monto = Decimal(str(monto))
        if self.cupTipo == 'PORCENTAJE':
            return (monto * Decimal(str(self.cupValor)) / 100).quantize(Decimal('0.01'))
        # VALOR_FIJO: no puede descontar más que el monto total
        return min(Decimal(str(self.cupValor)), monto)


class CuponAplicado(models.Model):
    # Tabla de auditoría: registra exactamente cuánto se descontó en el momento del pago.
    # No se puede recalcular después (el cupón puede cambiar de valor o desactivarse),
    # por eso se guarda montoDescontado como snapshot inmutable del descuento aplicado.
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
        # Previene doble-descuento: si el flujo de pago se ejecuta dos veces
        # (bug, doble-click, retry), la segunda inserción falla con IntegrityError
        # en lugar de aplicar el cupón dos veces y cobrar de menos al cliente.
        unique_together = [('fkIdPago', 'fkIdCupon')]

    def __str__(self):
        return f'Cupón {self.fkIdCupon.cupNombre} → Pago {self.fkIdPago.pk}'
