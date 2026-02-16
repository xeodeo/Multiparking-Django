from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fkIdVehiculo', 'fkIdEspacio', 'resFechaReserva', 'resHoraInicio', 'resHoraFin', 'resEstado')
    list_filter = ('resEstado', 'resFechaReserva')
