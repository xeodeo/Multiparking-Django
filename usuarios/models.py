from django.core.validators import RegexValidator
from django.db import models


# Modelo propio — NO usa django.contrib.auth.User
# La autenticación se maneja con sesiones manuales (session keys: usuario_id, usuario_rol, etc.)
class Usuario(models.Model):

    class RolChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'        # Acceso total al panel de administración
        VIGILANTE = 'VIGILANTE', 'Vigilante'    # Acceso al panel de guardia (/guardia/)
        CLIENTE = 'CLIENTE', 'Cliente'          # Acceso al dashboard del cliente (/dashboard/)

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
    usuCorreo = models.EmailField(max_length=64, unique=True)
    usuTelefono = models.CharField(
        max_length=10, blank=True,
        validators=[RegexValidator(r'^[0-9]+$', 'El teléfono solo debe contener números')],
    )
    usuClaveHash = models.CharField(max_length=255)  # Contraseña hasheada con django.contrib.auth.hashers.make_password
    rolTipoRol = models.CharField(
        max_length=10,
        choices=RolChoices.choices,
        default=RolChoices.CLIENTE,
    )
    usuEstado = models.BooleanField(default=True)  # False = cuenta desactivada (no puede iniciar sesión)
    usuFechaRegistro = models.DateTimeField(auto_now_add=True)

    @property
    def usuNombreCompleto(self):
        # Propiedad calculada — NO es columna de base de datos
        return f'{self.usuNombre} {self.usuApellido}'.strip()

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.usuDocumento} - {self.usuNombreCompleto}'
