from django.contrib import messages
from django.shortcuts import redirect


class AdminRequiredMixin:
    """Verifica que el usuario en sesión tenga rol ADMIN."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.error(request, 'Debes iniciar sesión.')
            return redirect('home')
        if request.session.get('usuario_rol') != 'ADMIN':
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
