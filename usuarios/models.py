from django.core.validators import RegexValidator
from django.db import models


class Usuario(models.Model):

    class RolChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        VIGILANTE = 'VIGILANTE', 'Vigilante'
        CLIENTE = 'CLIENTE', 'Cliente'

    usuDocumento = models.CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(r'^[0-9]+$', 'El documento solo debe contener números')],
    )
    usuNombre = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'El nombre solo debe contener letras')],
    )
    usuApellido = models.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', 'El apellido solo debe contener letras')],
    )
    usuCorreo = models.EmailField(unique=True)
    usuTelefono = models.CharField(
        max_length=10, blank=True,
        validators=[RegexValidator(r'^[0-9]+$', 'El teléfono solo debe contener números')],
    )
    usuClaveHash = models.CharField(max_length=255)
    rolTipoRol = models.CharField(
        max_length=10,
        choices=RolChoices.choices,
        default=RolChoices.CLIENTE,
    )
    usuEstado = models.BooleanField(default=True)
    usuFechaRegistro = models.DateTimeField(auto_now_add=True)

    @property
    def usuNombreCompleto(self):
        return f'{self.usuNombre} {self.usuApellido}'.strip()

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.usuDocumento} - {self.usuNombreCompleto}'
