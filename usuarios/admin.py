from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuDocumento', 'usuNombre', 'usuApellido', 'usuCorreo', 'rolTipoRol', 'usuEstado')
    list_filter = ('rolTipoRol', 'usuEstado')
    search_fields = ('usuDocumento', 'usuNombre', 'usuApellido', 'usuCorreo')
