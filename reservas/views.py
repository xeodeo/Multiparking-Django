from django.shortcuts import render
from django.views import View
from usuarios.mixins import AdminRequiredMixin
from .models import Reserva

class ReservaListView(AdminRequiredMixin, View):
    def get(self, request):
        reservas = Reserva.objects.select_related('fkIdVehiculo__fkIdUsuario', 'fkIdEspacio__fkIdPiso').order_by('-resFechaReserva', '-resHoraInicio')
        return render(request, 'admin_panel/reservas/list.html', {
            'active_page': 'reservas',
            'reservas': reservas
        })
