from django.core.validators import MinValueValidator
from django.db import models


class Tarifa(models.Model):
    nombre = models.CharField(max_length=50)
    fkIdTipoEspacio = models.ForeignKey(
        'parqueadero.TipoEspacio',
        on_delete=models.CASCADE,
        related_name='tarifas',
        db_column='fkIdTipoEspacio',
    )
    precioHora = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    # Precio diferenciado para visitantes (sin cuenta registrada) — generalmente mayor que precioHora
    precioHoraVisitante = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    precioDia = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    precioMensual = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    activa = models.BooleanField(default=True)  # Solo debe existir una tarifa activa por TipoEspacio a la vez (regla de negocio)
    fechaInicio = models.DateField()
    fechaFin = models.DateField(null=True, blank=True)  # null = tarifa vigente indefinidamente

    class Meta:
        db_table = 'tarifas'
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'

    def __str__(self):
        return f'{self.nombre} - {self.fkIdTipoEspacio.nombre}'
