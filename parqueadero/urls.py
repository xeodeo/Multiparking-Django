from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # Pisos
    path('pisos/', views.PisoListView.as_view(), name='admin_pisos'),
    path('pisos/crear/', views.PisoCreateView.as_view(), name='admin_pisos_crear'),
    path('pisos/editar/<int:pk>/', views.PisoUpdateView.as_view(), name='admin_pisos_editar'),
    path('pisos/eliminar/<int:pk>/', views.PisoDeleteView.as_view(), name='admin_pisos_eliminar'),
    
    # Tipos de Espacio
    path('tipos-espacio/', views.TipoEspacioListView.as_view(), name='admin_tipos_espacio'),
    path('tipos-espacio/crear/', views.TipoEspacioCreateView.as_view(), name='admin_tipos_espacio_crear'),
    path('tipos-espacio/editar/<int:pk>/', views.TipoEspacioUpdateView.as_view(), name='admin_tipos_espacio_editar'),
    path('tipos-espacio/eliminar/<int:pk>/', views.TipoEspacioDeleteView.as_view(), name='admin_tipos_espacio_eliminar'),

    # Espacios
    path('espacios/', views.EspacioListView.as_view(), name='admin_espacios'),
    path('espacios/crear/', views.EspacioCreateView.as_view(), name='admin_espacios_crear'),
    path('espacios/editar/<int:pk>/', views.EspacioUpdateView.as_view(), name='admin_espacios_editar'),
    path('espacios/eliminar/<int:pk>/', views.EspacioDeleteView.as_view(), name='admin_espacios_eliminar'),
    path('espacios/rango/', views.EspacioRangeCreateView.as_view(), name='admin_espacios_rango'),
    
    # Tarifas (Placeholder URLs - need implementation in views.py but defining here)
    # path('tarifas/', views.TarifaListView.as_view(), name='admin_tarifas'),
    # path('tarifas/crear/', views.TarifaCreateView.as_view(), name='admin_tarifas_crear'),
    # path('tarifas/eliminar/<int:pk>/', views.TarifaDeleteView.as_view(), name='admin_tarifas_eliminar'),
    
    # Cupones (Placeholder URLs)
    # path('cupones/', views.CuponListView.as_view(), name='admin_cupones'),
    # path('cupones/crear/', views.CuponCreateView.as_view(), name='admin_cupones_crear'),
    # path('cupones/eliminar/<int:pk>/', views.CuponDeleteView.as_view(), name='admin_cupones_eliminar'),

    # Reservas (Placeholder)
    # path('reservas/', views.ReservaListView.as_view(), name='admin_reservas'),

    # Operaciones
    path('registrar-ingreso/', views.RegistrarIngresoView.as_view(), name='admin_registrar_ingreso'),
    path('registrar-salida/', views.RegistrarSalidaView.as_view(), name='admin_registrar_salida'),
    path('api/buscar-vehiculo/', views.BuscarVehiculoView.as_view(), name='admin_buscar_vehiculo'),
    path('api/detalle-ocupacion/', views.ObtenerDetalleOcupacionView.as_view(), name='admin_detalle_ocupacion'),
]
