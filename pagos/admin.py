from django.contrib import admin

from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pagMonto', 'pagMetodo', 'pagEstado', 'pagFechaPago', 'fkIdParqueo')
    list_filter = ('pagEstado', 'pagMetodo')
