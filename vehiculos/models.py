from django.db import models


class Vehiculo(models.Model):

    class TipoChoices(models.TextChoices):
        CARRO = 'CARRO', 'Carro'
        MOTO = 'MOTO', 'Moto'

    vehPlaca = models.CharField(max_length=10, unique=True)
    vehTipo = models.CharField(
        max_length=30,
        choices=TipoChoices.choices,
        default=TipoChoices.CARRO,
    )
    vehColor = models.CharField(max_length=30, blank=True)
    vehMarca = models.CharField(max_length=50, blank=True)
    vehModelo = models.CharField(max_length=50, blank=True)
    vehEstado = models.BooleanField(default=True)
    fkIdUsuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='vehiculos',
        db_column='fkIdUsuario',
        null=True,
        blank=True
    )
    es_visitante = models.BooleanField(default=True)
    nombre_contacto = models.CharField(max_length=100, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        indexes = [
            models.Index(fields=['vehPlaca'], name='idx_vehiculo_placa'),
        ]

    def __str__(self):
        return f'{self.vehPlaca} - {self.vehMarca} {self.vehModelo}'
