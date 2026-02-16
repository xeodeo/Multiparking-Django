from django.contrib import admin

from .models import Espacio, InventarioParqueo, Piso, TipoEspacio


@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    list_display = ('pisNombre', 'pisEstado')
    list_filter = ('pisEstado',)


@admin.register(TipoEspacio)
class TipoEspacioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ('espNumero', 'fkIdPiso', 'fkIdTipoEspacio', 'espEstado')
    list_filter = ('espEstado', 'fkIdPiso', 'fkIdTipoEspacio')
    search_fields = ('espNumero',)


@admin.register(InventarioParqueo)
class InventarioParqueoAdmin(admin.ModelAdmin):
    list_display = ('fkIdVehiculo', 'fkIdEspacio', 'parHoraEntrada', 'parHoraSalida')
    list_filter = ('parHoraSalida',)
