from django.core.validators import RegexValidator
from django.db import models


class Vehiculo(models.Model):

    class TipoChoices(models.TextChoices):
        CARRO = 'Carro', 'Carro'
        MOTO = 'Moto', 'Moto'

    vehPlaca = models.CharField(
        max_length=8, unique=True,
        validators=[RegexValidator(r'^[A-Za-z0-9-]+$', 'La placa solo acepta letras, números y guiones')],
    )
    vehTipo = models.CharField(
        max_length=5,
        choices=TipoChoices.choices,
        default=TipoChoices.CARRO,
    )
    vehColor = models.CharField(
        max_length=20, blank=True,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'El color solo debe contener letras')],
    )
    vehMarca = models.CharField(
        max_length=30, blank=True,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+$', 'La marca solo acepta letras y números')],
    )
    vehModelo = models.CharField(
        max_length=30, blank=True,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.\-]+$', 'El modelo solo acepta letras, números y puntos')],
    )
    vehEstado = models.BooleanField(default=True)
    fkIdUsuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='vehiculos',
        db_column='fkIdUsuario',
        null=True,
        blank=True
    )
    nombre_contacto = models.CharField(
        max_length=50, null=True, blank=True,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'El nombre solo debe contener letras')],
    )
    telefono_contacto = models.CharField(
        max_length=10, null=True, blank=True,
        validators=[RegexValidator(r'^[0-9]+$', 'El teléfono solo debe contener números')],
    )

    @property
    def es_visitante(self):
        return self.fkIdUsuario_id is None

    class Meta:
        db_table = 'vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        indexes = [
            models.Index(fields=['vehPlaca'], name='idx_vehiculo_placa'),
        ]

    def __str__(self):
        return f'{self.vehPlaca} - {self.vehMarca} {self.vehModelo}'
