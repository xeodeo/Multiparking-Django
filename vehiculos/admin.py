from django.contrib import admin

from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehPlaca', 'vehTipo', 'vehMarca', 'vehModelo', 'vehColor', 'fkIdUsuario')
    search_fields = ('vehPlaca', 'vehMarca')
    list_filter = ('vehTipo',)
