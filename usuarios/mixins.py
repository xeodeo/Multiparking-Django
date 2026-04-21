from django.contrib import messages
from django.shortcuts import redirect

# Mapa de rol → URL de destino tras login/registro exitoso.
# Centralizado aquí para evitar strings hardcodeados en múltiples vistas.
ROL_REDIRECT_URL = {
    'ADMIN':     '/admin-panel/',
    'VIGILANTE': '/guardia/',
    'CLIENTE':   '/dashboard/',
}


def _no_cache(response):
    # Forzar no-cacheo en todas las respuestas autenticadas: previene que al presionar
    # "atrás" tras cerrar sesión el navegador muestre una página cacheada del panel.
    # No se aplica a páginas públicas (home, login) — esas sí pueden cachearse.
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


class AdminRequiredMixin:
    """Verifica que el usuario en sesión tenga rol ADMIN."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('home')
        if request.session.get('usuario_rol') != 'ADMIN':
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('dashboard')
        # _no_cache se aplica aquí (en el mixin, no en cada vista) para que ninguna
        # vista de admin olvide el header. El type: ignore es porque View.dispatch
        # no está tipado en los stubs de Django y mypy no puede inferirlo.
        return _no_cache(super().dispatch(request, *args, **kwargs))  # type: ignore[attr-defined]


class VigilanteRequiredMixin:
    """Verifica que el usuario en sesión tenga rol ADMIN o VIGILANTE."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('home')
        if request.session.get('usuario_rol') not in ('ADMIN', 'VIGILANTE'):
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('dashboard')
        return _no_cache(super().dispatch(request, *args, **kwargs))  # type: ignore[attr-defined]


class ClienteRequiredMixin:
    """Verifica que el usuario esté autenticado (cualquier rol)."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)  # type: ignore[attr-defined]
