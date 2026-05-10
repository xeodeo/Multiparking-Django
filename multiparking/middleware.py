from django.db import OperationalError, ProgrammingError
from django.http import HttpResponse


def _render_500():
    try:
        with open('templates/500.html', 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), status=500, content_type='text/html')
    except Exception:
        return HttpResponse(
            '<h1 style="font-family:sans-serif;color:#fff;background:#0a0a14;padding:2rem">Error del servidor (500)</h1>',
            status=500, content_type='text/html'
        )


class DatabaseErrorMiddleware:
    """
    Captura errores de base de datos (OperationalError, ProgrammingError) en cualquier
    vista y devuelve la página 500 estática sin depender del ORM ni de templates dinámicos.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except (OperationalError, ProgrammingError):
            return _render_500()

    def process_exception(self, _request, exception):
        if isinstance(exception, (OperationalError, ProgrammingError)):
            return _render_500()
        return None


class SecurityHeadersMiddleware:
    """
    Agrega headers de seguridad HTTP a todas las respuestas:
    - Content-Security-Policy: restringe orígenes de scripts/estilos
    - X-XSS-Protection: activa el filtro XSS del navegador
    """

    CSP = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://cdn.tailwindcss.com "
        "https://cdn.jsdelivr.net "
        "https://cdnjs.cloudflare.com "
        "https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' "
        "https://cdn.tailwindcss.com "
        "https://cdn.jsdelivr.net "
        "https://cdnjs.cloudflare.com; "
        "img-src 'self' data: blob:; "
        "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = self.CSP
        response['X-XSS-Protection'] = '1; mode=block'
        return response


class NoCacheAfterLogoutMiddleware:
    """
    Agrega headers Cache-Control a las respuestas de usuarios autenticados
    para que el navegador no muestre páginas cacheadas al presionar 'atrás'
    después de cerrar sesión.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.session.get('usuario_id'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
