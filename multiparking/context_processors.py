
def cuponera_context(request):
    """Indica si el cliente tiene un cupón bono activo para mostrar la cuponera."""
    if request.session.get('usuario_rol') != 'CLIENTE':
        return {}
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return {}
    try:
        from usuarios.models import Usuario
        from cupones.models import Cupon
        usuario = Usuario.objects.get(pk=usuario_id)
        tiene_cuponera = Cupon.objects.filter(
            cupCodigo__startswith='BONO',
            cupActivo=True,
            cupNombre__icontains=usuario.usuNombreCompleto,
        ).exists()
    except Exception:
        tiene_cuponera = False
    return {'tiene_cuponera': tiene_cuponera}
