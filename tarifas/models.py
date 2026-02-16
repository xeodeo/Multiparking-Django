from django.db import models


class Tarifa(models.Model):
    nombre = models.CharField(max_length=100)
    fkIdTipoEspacio = models.ForeignKey(
        'parqueadero.TipoEspacio',
        on_delete=models.CASCADE,
        related_name='tarifas',
        db_column='fkIdTipoEspacio',
    )
    precioHora = models.DecimalField(max_digits=10, decimal_places=2)
    precioDia = models.DecimalField(max_digits=10, decimal_places=2)
    precioMensual = models.DecimalField(max_digits=12, decimal_places=2)
    activa = models.BooleanField(default=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tarifas'
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'

    def __str__(self):
        return f'{self.nombre} - {self.fkIdTipoEspacio.nombre}'
