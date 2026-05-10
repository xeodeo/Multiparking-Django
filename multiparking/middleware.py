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
