from django.urls import path
from .views import ReservaDetallesAPIView

urlpatterns = [
    path('<int:pk>/detalles/', ReservaDetallesAPIView.as_view(), name='api_reserva_detalles'),
]
