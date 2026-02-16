from django.contrib import admin

from .models import Cupon, CuponAplicado


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('cupNombre', 'cupTipo', 'cupValor', 'cupFechaInicio', 'cupFechaFin', 'cupActivo')
    list_filter = ('cupTipo', 'cupActivo')


@admin.register(CuponAplicado)
class CuponAplicadoAdmin(admin.ModelAdmin):
    list_display = ('fkIdPago', 'fkIdCupon', 'montoDescontado')
