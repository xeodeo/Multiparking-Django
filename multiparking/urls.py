from django.contrib import admin
from django.urls import include, path

from usuarios.views import (
    dashboard_view,
    home_view,
    login_view,
    logout_view,
    register_view,
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView, UsuarioToggleView,
)
from parqueadero.views import (
    AdminDashboardView,
    PisoListView, PisoCreateView, PisoUpdateView, PisoDeleteView,
    TipoEspacioListView, TipoEspacioCreateView, TipoEspacioUpdateView, TipoEspacioDeleteView,
    EspacioListView, EspacioCreateView, EspacioUpdateView, EspacioDeleteView, EspacioRangeCreateView,
    InventarioListView,
    EntradaParqueaderoView, EscanearQRView, GenerarQRView
)
from tarifas.views import (
    TarifaListView, TarifaCreateView, TarifaUpdateView, TarifaToggleView, TarifaDeleteView
)
from cupones.views import (
    CuponListView, CuponCreateView, CuponUpdateView, CuponDeleteView
)
from reservas.views import ReservaListView, ReservaFinalizarView, ReservaCancelarView
from vehiculos.views import (
    VehiculoListView, VehiculoCreateView, VehiculoUpdateView, VehiculoDeleteView
)
from pagos.views import PagosListView
from parqueadero.reportes_views import ReportesView, ExportarPDFReportesView, ExportarExcelReportesView
from vehiculos.cliente_views import ClienteCrearVehiculoView, ClienteEditarVehiculoView
from reservas.cliente_views import (
    ClienteCrearReservaView, ClienteEditarReservaView,
    ClienteCancelarReservaView, ClienteConfirmarReservaView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Páginas principales
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # API endpoints
    path('api/usuarios/', include('usuarios.urls')),
    path('api/vehiculos/', include('vehiculos.urls')),
    path('api/parqueadero/', include('parqueadero.urls')),
    path('api/tarifas/', include('tarifas.urls')),
    path('api/pagos/', include('pagos.urls')),
    path('api/cupones/', include('cupones.urls')),
    path('api/reservas/', include('reservas.urls')),

    # ── ADMIN PANEL ──────────────────────────────────────────────────

    # Dashboard
    path('admin-panel/', AdminDashboardView.as_view(), name='admin_dashboard'),

    # Pisos
    path('admin-panel/pisos/', PisoListView.as_view(), name='admin_pisos'),
    path('admin-panel/pisos/crear/', PisoCreateView.as_view(), name='admin_pisos_crear'),
    path('admin-panel/pisos/<int:pk>/editar/', PisoUpdateView.as_view(), name='admin_pisos_editar'),
    path('admin-panel/pisos/<int:pk>/eliminar/', PisoDeleteView.as_view(), name='admin_pisos_eliminar'),

    # Tipos de Espacio
    path('admin-panel/tipos-espacio/', TipoEspacioListView.as_view(), name='admin_tipos_espacio'),
    path('admin-panel/tipos-espacio/crear/', TipoEspacioCreateView.as_view(), name='admin_tipos_espacio_crear'),
    path('admin-panel/tipos-espacio/<int:pk>/editar/', TipoEspacioUpdateView.as_view(), name='admin_tipos_espacio_editar'),
    path('admin-panel/tipos-espacio/<int:pk>/eliminar/', TipoEspacioDeleteView.as_view(), name='admin_tipos_espacio_eliminar'),

    # Espacios
    path('admin-panel/espacios/', EspacioListView.as_view(), name='admin_espacios'),
    path('admin-panel/espacios/crear/', EspacioCreateView.as_view(), name='admin_espacios_crear'),
    path('admin-panel/espacios/rango/', EspacioRangeCreateView.as_view(), name='admin_espacios_rango'),
    path('admin-panel/espacios/<int:pk>/editar/', EspacioUpdateView.as_view(), name='admin_espacios_editar'),
    path('admin-panel/espacios/<int:pk>/eliminar/', EspacioDeleteView.as_view(), name='admin_espacios_eliminar'),

    # Tarifas
    path('admin-panel/tarifas/', TarifaListView.as_view(), name='admin_tarifas'),
    path('admin-panel/tarifas/crear/', TarifaCreateView.as_view(), name='admin_tarifas_crear'),
    path('admin-panel/tarifas/<int:pk>/editar/', TarifaUpdateView.as_view(), name='admin_tarifas_editar'),
    path('admin-panel/tarifas/<int:pk>/toggle/', TarifaToggleView.as_view(), name='admin_tarifas_toggle'),
    path('admin-panel/tarifas/<int:pk>/eliminar/', TarifaDeleteView.as_view(), name='admin_tarifas_eliminar'),

    # Cupones
    path('admin-panel/cupones/', CuponListView.as_view(), name='admin_cupones'),
    path('admin-panel/cupones/crear/', CuponCreateView.as_view(), name='admin_cupones_crear'),
    path('admin-panel/cupones/<int:pk>/editar/', CuponUpdateView.as_view(), name='admin_cupones_editar'),
    path('admin-panel/cupones/<int:pk>/eliminar/', CuponDeleteView.as_view(), name='admin_cupones_eliminar'),

    # Vehículos
    path('admin-panel/vehiculos/', VehiculoListView.as_view(), name='admin_vehiculos'),
    path('admin-panel/vehiculos/crear/', VehiculoCreateView.as_view(), name='admin_vehiculos_crear'),
    path('admin-panel/vehiculos/<int:pk>/editar/', VehiculoUpdateView.as_view(), name='admin_vehiculos_editar'),
    path('admin-panel/vehiculos/<int:pk>/eliminar/', VehiculoDeleteView.as_view(), name='admin_vehiculos_eliminar'),

    # Reservas
    path('admin-panel/reservas/', ReservaListView.as_view(), name='admin_reservas'),
    path('admin-panel/reservas/<int:pk>/finalizar/', ReservaFinalizarView.as_view(), name='admin_reservas_finalizar'),
    path('admin-panel/reservas/<int:pk>/cancelar/', ReservaCancelarView.as_view(), name='admin_reservas_cancelar'),

    # Inventario
    path('admin-panel/inventario/', InventarioListView.as_view(), name='admin_inventario'),

    # Pagos
    path('admin-panel/pagos/', PagosListView.as_view(), name='admin_pagos'),

    # Reportes
    path('admin-panel/reportes/', ReportesView.as_view(), name='admin_reportes'),
    path('admin-panel/reportes/exportar-pdf/', ExportarPDFReportesView.as_view(), name='admin_reportes_pdf'),
    path('admin-panel/reportes/exportar-excel/', ExportarExcelReportesView.as_view(), name='admin_reportes_excel'),

    # Usuarios
    path('admin-panel/usuarios/', UsuarioListView.as_view(), name='admin_usuarios'),
    path('admin-panel/usuarios/crear/', UsuarioCreateView.as_view(), name='admin_usuarios_crear'),
    path('admin-panel/usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='admin_usuarios_editar'),
    path('admin-panel/usuarios/<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='admin_usuarios_eliminar'),
    path('admin-panel/usuarios/<int:pk>/toggle/', UsuarioToggleView.as_view(), name='admin_usuarios_toggle'),

    # Código QR
    path('admin-panel/qr/generar/', GenerarQRView.as_view(), name='admin_generar_qr'),

    # ── CLIENTE PANEL ────────────────────────────────────────────────────

    # Entrada al Parqueadero
    path('parqueadero/escanear/', EscanearQRView.as_view(), name='escanear_qr'),
    path('parqueadero/entrada/', EntradaParqueaderoView.as_view(), name='entrada_parqueadero'),

    # Vehículos del Cliente
    path('cliente/vehiculos/crear/', ClienteCrearVehiculoView.as_view(), name='cliente_crear_vehiculo'),
    path('cliente/vehiculos/<int:pk>/editar/', ClienteEditarVehiculoView.as_view(), name='cliente_editar_vehiculo'),

    # Reservas del Cliente
    path('cliente/reservas/crear/', ClienteCrearReservaView.as_view(), name='cliente_crear_reserva'),
    path('cliente/reservas/<int:pk>/editar/', ClienteEditarReservaView.as_view(), name='cliente_editar_reserva'),
    path('cliente/reservas/<int:pk>/cancelar/', ClienteCancelarReservaView.as_view(), name='cliente_cancelar_reserva'),
    path('cliente/reservas/<int:pk>/confirmar/', ClienteConfirmarReservaView.as_view(), name='cliente_confirmar_reserva'),
]
