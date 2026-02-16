from django.db import models


class Usuario(models.Model):

    class RolChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        VIGILANTE = 'VIGILANTE', 'Vigilante'
        CLIENTE = 'CLIENTE', 'Cliente'

    usuDocumento = models.CharField(max_length=20, unique=True)
    usuNombreCompleto = models.CharField(max_length=150)
    usuCorreo = models.EmailField(unique=True)
    usuTelefono = models.CharField(max_length=20, blank=True)
    usuClaveHash = models.CharField(max_length=255)
    rolTipoRol = models.CharField(
        max_length=10,
        choices=RolChoices.choices,
        default=RolChoices.CLIENTE,
    )
    usuEstado = models.BooleanField(default=True)
    usuFechaRegistro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.usuDocumento} - {self.usuNombreCompleto}'
