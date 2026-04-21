import re

RE_PLACA = re.compile(r'^[A-Za-z0-9-]+$')
RE_SOLO_LETRAS = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
RE_LETRAS_NUMEROS = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+$')
RE_MODELO = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.\-]+$')
RE_SOLO_NUMEROS = re.compile(r'^[0-9]+$')


def validar_datos_vehiculo(placa, tipo, color='', marca='', modelo='',
                           nombre_contacto='', telefono_contacto=''):
    """
    Valida los campos de un vehículo.
    Devuelve None si todo es válido, o un mensaje de error como string.
    """
    if not placa or not tipo:
        return 'Placa y tipo son obligatorios.'
    if not RE_PLACA.match(placa):
        return 'La placa solo acepta letras, números y guiones.'
    if color and not RE_SOLO_LETRAS.match(color):
        return 'El color solo debe contener letras.'
    if marca and not RE_LETRAS_NUMEROS.match(marca):
        return 'La marca solo acepta letras y números.'
    if modelo and not RE_MODELO.match(modelo):
        return 'El modelo solo acepta letras, números y puntos.'
    if nombre_contacto and not RE_SOLO_LETRAS.match(nombre_contacto):
        return 'El nombre de contacto solo debe contener letras.'
    if telefono_contacto and not RE_SOLO_NUMEROS.match(telefono_contacto):
        return 'El teléfono de contacto solo debe contener números.'
    return None
