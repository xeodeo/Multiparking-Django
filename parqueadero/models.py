from django.core.validators import RegexValidator
from django.db import models


class Piso(models.Model):
    pisNombre = models.CharField(
        max_length=30,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-]+$', 'El nombre solo acepta letras, números y guiones')],
    )
    pisEstado = models.BooleanField(default=True)  # True = activo, False = desactivado (ej. en mantenimiento)

    class Meta:
        db_table = 'pisos'
        verbose_name = 'Piso'
        verbose_name_plural = 'Pisos'

    def __str__(self):
        return self.pisNombre


class TipoEspacio(models.Model):
    # Categoría del espacio: 'Carro' o 'Moto' — determina qué tarifa aplica
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'tipos_espacio'
        verbose_name = 'Tipo de Espacio'
        verbose_name_plural = 'Tipos de Espacio'

    def __str__(self):
        return self.nombre


class Espacio(models.Model):

    class EstadoChoices(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'  # Libre para recibir vehículos
        OCUPADO = 'OCUPADO', 'Ocupado'            # Hay un vehículo estacionado
        INACTIVO = 'INACTIVO', 'Inactivo'         # Fuera de servicio (mantenimiento, etc.)

    espNumero = models.CharField(max_length=10)  # Código único del puesto, ej. 'C1-01', 'M2-05'
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
        max_length=10,
        choices=EstadoChoices.choices,
        default=EstadoChoices.DISPONIBLE,
    )

    class Meta:
        db_table = 'espacios'
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'
        unique_together = [('fkIdPiso', 'espNumero')]  # El mismo número no puede repetirse dentro de un piso
        indexes = [
            models.Index(fields=['espNumero'], name='idx_espacio_numero'),
        ]

    def __str__(self):
        return f'{self.espNumero} - Piso {self.fkIdPiso}'


class InventarioParqueo(models.Model):
    parHoraEntrada = models.DateTimeField(auto_now_add=True)              # Se asigna automáticamente al crear el registro
    parHoraSalida = models.DateTimeField(null=True, blank=True)            # NULL = vehículo aún estacionado; con valor = ya salió
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
            # Índice en parHoraSalida para filtrar eficientemente los vehículos activos (parHoraSalida IS NULL)
            models.Index(fields=['parHoraSalida'], name='idx_parqueo_estado'),
        ]

    def __str__(self):
        estado = 'Activo' if self.parHoraSalida is None else 'Finalizado'
        return f'{self.fkIdVehiculo.vehPlaca} - {estado}'
