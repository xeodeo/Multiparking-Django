from django.contrib import messages
from django.shortcuts import redirect


def _no_cache(response):
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


class AdminRequiredMixin:
    """Verifica que el usuario en sesión tenga rol ADMIN."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('home')
        if request.session.get('usuario_rol') != 'ADMIN':
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('dashboard')
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
