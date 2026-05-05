from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from usuarios.views import (
    dashboard_view,
    home_view,
    login_view,
    logout_view,
    register_view,
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView, UsuarioToggleView,
    PasswordResetRequestView, PasswordResetConfirmView,
    AdminTestEmailView,
)
from parqueadero.views import (
    AdminDashboardView, AdminDashboardDataView,
    PisoListView, PisoCreateView, PisoUpdateView, PisoDeleteView,
    TipoEspacioListView, TipoEspacioCreateView, TipoEspacioUpdateView, TipoEspacioDeleteView,
    EspacioListView, EspacioCreateView, EspacioUpdateView, EspacioDeleteView, EspacioRangeCreateView,
    InventarioListView,
    EntradaParqueaderoView, EscanearQRView, GenerarQRView
)
from parqueadero.vigilante_views import (
    VigilanteDashboardView, VigilanteDashboardDataView,
    VigilanteRegistrarIngresoView, VigilanteRegistrarSalidaView,
    VigilanteConfirmarPagoView, VigilanteBuscarVehiculoView,
    VigilanteObtenerDetalleView,
)
from parqueadero.cliente_views import ClienteSalidaView
from tarifas.views import (
    TarifaListView, TarifaCreateView, TarifaUpdateView, TarifaToggleView, TarifaDeleteView
)
from cupones.views import (
    CuponListView, CuponCreateView, CuponUpdateView, CuponDeleteView
)
from reservas.views import ReservaListView, ReservaFinalizarView, ReservaCancelarView, ReservaEditarView
from novedades.views import NovedadListView, NovedadCreateView, NovedadUpdateView, NovedadDeleteView
from fidelidad.views import FidelidadConfigView, PerfilClienteView, ReclamarBonoView
from vehiculos.views import (
    VehiculoListView, VehiculoCreateView, VehiculoUpdateView, VehiculoDeleteView
)
from pagos.views import PagosListView, ReciboView
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
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
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
    path('admin-panel/api/dashboard-data/', AdminDashboardDataView.as_view(), name='admin_dashboard_data'),

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
    path('admin-panel/reservas/<int:pk>/editar/', ReservaEditarView.as_view(), name='admin_reservas_editar'),
    # Novedades
    path('admin-panel/novedades/', NovedadListView.as_view(), name='admin_novedades'),
    path('admin-panel/novedades/crear/', NovedadCreateView.as_view(), name='admin_novedades_crear'),
    path('admin-panel/novedades/<int:pk>/editar/', NovedadUpdateView.as_view(), name='admin_novedades_editar'),
    path('admin-panel/novedades/<int:pk>/eliminar/', NovedadDeleteView.as_view(), name='admin_novedades_eliminar'),
    # Fidelidad
    path('admin-panel/fidelidad/', FidelidadConfigView.as_view(), name='admin_fidelidad'),
    path('cliente/perfil/', PerfilClienteView.as_view(), name='cliente_perfil'),
    path('cliente/perfil/reclamar-bono/', ReclamarBonoView.as_view(), name='cliente_reclamar_bono'),

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

    # Prueba de correos
    path('admin-panel/test-email/', AdminTestEmailView.as_view(), name='admin_test_email'),

    # ── GUARDIA PANEL ────────────────────────────────────────────────────

    path('guardia/', VigilanteDashboardView.as_view(), name='guardia_dashboard'),
    path('guardia/api/data/', VigilanteDashboardDataView.as_view(), name='guardia_data'),
    path('guardia/registrar-ingreso/', VigilanteRegistrarIngresoView.as_view(), name='guardia_registrar_ingreso'),
    path('guardia/registrar-salida/', VigilanteRegistrarSalidaView.as_view(), name='guardia_registrar_salida'),
    path('guardia/confirmar-pago/', VigilanteConfirmarPagoView.as_view(), name='guardia_confirmar_pago'),
    path('guardia/api/buscar-vehiculo/', VigilanteBuscarVehiculoView.as_view(), name='guardia_buscar_vehiculo'),
    path('guardia/api/detalle-ocupacion/', VigilanteObtenerDetalleView.as_view(), name='guardia_detalle_ocupacion'),

    # ── CLIENTE PANEL ────────────────────────────────────────────────────

    # Entrada al Parqueadero
    path('parqueadero/escanear/', EscanearQRView.as_view(), name='escanear_qr'),
    path('parqueadero/entrada/', EntradaParqueaderoView.as_view(), name='entrada_parqueadero'),
    path('parqueadero/salida/', ClienteSalidaView.as_view(), name='cliente_salida'),

    # Vehículos del Cliente
    path('cliente/vehiculos/crear/', ClienteCrearVehiculoView.as_view(), name='cliente_crear_vehiculo'),
    path('cliente/vehiculos/<int:pk>/editar/', ClienteEditarVehiculoView.as_view(), name='cliente_editar_vehiculo'),

    # Reservas del Cliente
    path('cliente/reservas/crear/', ClienteCrearReservaView.as_view(), name='cliente_crear_reserva'),
    path('cliente/reservas/<int:pk>/editar/', ClienteEditarReservaView.as_view(), name='cliente_editar_reserva'),
    path('cliente/reservas/<int:pk>/cancelar/', ClienteCancelarReservaView.as_view(), name='cliente_cancelar_reserva'),
    path('cliente/reservas/<int:pk>/confirmar/', ClienteConfirmarReservaView.as_view(), name='cliente_confirmar_reserva'),
    # Recibo de pago (acceso por rol)
    path('recibo/<int:pk>/', ReciboView.as_view(), name='recibo_pago'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'multiparking.error_views.error_404'
handler500 = 'multiparking.error_views.error_500'
handler403 = 'multiparking.error_views.error_403'
