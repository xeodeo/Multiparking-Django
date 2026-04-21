import re

RE_SOLO_NUMEROS = re.compile(r'^[0-9]+$')
RE_SOLO_LETRAS  = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
RE_CORREO       = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')


def validar_datos_usuario(documento, nombre, apellido, correo, telefono='', clave='', clave_confirm=None):
    """
    Valida los campos comunes de usuario.
    Retorna (True, None) si válido; (False, 'mensaje') si no.
    clave_confirm=None → no valida confirmación de contraseña.
    """
    if not all([documento, nombre, apellido, correo]):
        return False, 'Documento, nombre, apellido y correo son obligatorios.'

    if len(documento) < 6:
        return False, 'El documento debe tener al menos 6 caracteres.'

    if not RE_SOLO_NUMEROS.match(documento):
        return False, 'El documento solo debe contener números.'

    if not RE_SOLO_LETRAS.match(nombre):
        return False, 'El nombre solo debe contener letras.'

    if not RE_SOLO_LETRAS.match(apellido):
        return False, 'El apellido solo debe contener letras.'

    if telefono and not RE_SOLO_NUMEROS.match(telefono):
        return False, 'El teléfono solo debe contener números.'

    if not RE_CORREO.match(correo):
        return False, 'Ingresa un correo válido (ej: usuario@dominio.com).'

    if clave:
        if len(clave) < 6:
            return False, 'La contraseña debe tener al menos 6 caracteres.'
        if clave_confirm is not None and clave != clave_confirm:
            return False, 'Las contraseñas no coinciden.'

    return True, None
