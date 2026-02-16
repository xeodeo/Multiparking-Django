from django.db import models


class Piso(models.Model):
    pisNombre = models.CharField(max_length=50)
    pisEstado = models.BooleanField(default=True)

    class Meta:
        db_table = 'pisos'
        verbose_name = 'Piso'
        verbose_name_plural = 'Pisos'

    def __str__(self):
        return self.pisNombre


class TipoEspacio(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tipos_espacio'
        verbose_name = 'Tipo de Espacio'
        verbose_name_plural = 'Tipos de Espacio'

    def __str__(self):
        return self.nombre


class Espacio(models.Model):

    class EstadoChoices(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        OCUPADO = 'OCUPADO', 'Ocupado'
        INACTIVO = 'INACTIVO', 'Inactivo'

    espNumero = models.CharField(max_length=20)
    fkIdPiso = models.ForeignKey(
        Piso,
        on_delete=models.CASCADE,
        related_name='espacios',
        db_column='fkIdPiso',
    )
    fkIdTipoEspacio = models.ForeignKey(
        TipoEspacio,
        on_delete=models.CASCADE,
        related_name='espacios',
        db_column='fkIdTipoEspacio',
    )
    espEstado = models.CharField(
        max_length=11,
        choices=EstadoChoices.choices,
        default=EstadoChoices.DISPONIBLE,
    )

    class Meta:
        db_table = 'espacios'
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'
        indexes = [
            models.Index(fields=['espNumero'], name='idx_espacio_numero'),
        ]

    def __str__(self):
        return f'{self.espNumero} - Piso {self.fkIdPiso}'


class InventarioParqueo(models.Model):
    parHoraEntrada = models.DateTimeField(auto_now_add=True)
    parHoraSalida = models.DateTimeField(null=True, blank=True)
    fkIdVehiculo = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.CASCADE,
        related_name='parqueos',
        db_column='fkIdVehiculo',
    )
    fkIdEspacio = models.ForeignKey(
        Espacio,
        on_delete=models.CASCADE,
        related_name='parqueos',
        db_column='fkIdEspacio',
    )

    class Meta:
        db_table = 'inventario_parqueo'
        verbose_name = 'Inventario Parqueo'
        verbose_name_plural = 'Inventario Parqueo'
        indexes = [
            models.Index(fields=['parHoraSalida'], name='idx_parqueo_estado'),
        ]

    def __str__(self):
        estado = 'Activo' if self.parHoraSalida is None else 'Finalizado'
        return f'{self.fkIdVehiculo.vehPlaca} - {estado}'
