"""
Validators compartidos entre apps.
Centraliza funciones de validación para evitar duplicación entre tarifas/views.py
y cupones/views.py (que tenían versiones ligeramente distintas de la misma función).
"""
from decimal import Decimal, InvalidOperation


def validar_decimal_positivo(valor, campo='El valor'):
    """
    Parsea y valida un valor decimal positivo.

    Retorna (Decimal, None) si es válido, o (None, mensaje_error) si no lo es.

    Args:
        valor: string o valor a parsear como Decimal
        campo: nombre del campo para el mensaje de error (ej. 'Precio hora')
    """
    try:
        resultado = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        return None, f'{campo}: debe ser un número válido.'
    if resultado < 0:
        return None, f'{campo}: no puede ser negativo.'
    return resultado, None
