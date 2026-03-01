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
