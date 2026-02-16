from django.contrib import admin

from .models import Tarifa


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fkIdTipoEspacio', 'precioHora', 'precioDia', 'precioMensual', 'activa')
    list_filter = ('activa', 'fkIdTipoEspacio')
