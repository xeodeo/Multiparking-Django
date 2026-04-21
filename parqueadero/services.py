import math

from django.utils import timezone

STICKER_MIN_MINUTOS = 60  # Mínimo de minutos para ganar un sticker de fidelidad


def calcular_costo_parqueo(hora_entrada, tarifa, vehiculo, hora_salida=None):
    """
    Calcula el costo de un turno de parqueo.

    - hora_salida=None → usa timezone.now(); permite mostrar costo acumulado
      en tiempo real en el dashboard sin cerrar el turno.
    - Redondea hacia arriba con la fórmula `(seg + 59) // 60` en lugar de
      math.ceil(seg/60), porque ceil(0) = 0 y queremos mínimo 1 minuto.
    - Mínimo 1 minuto: evita cobros de $0 si el sistema registra entrada/salida
      con menos de 1 segundo de diferencia (ej. error de doble-click en el guardia).
    - Visitantes pagan precioHoraVisitante cuando está configurado (> 0); si vale 0
      se interpreta como "sin diferenciación de precio" y se usa precioHora normal.
    """
    ahora = hora_salida or timezone.now()
    # +59 en el numerador hace que cualquier fracción de minuto cuente como minuto
    # completo (ej: 61 segundos → (61+59)//60 = 2 min, no 1.016 min redondeado).
    total_minutos = max((int((ahora - hora_entrada).total_seconds()) + 59) // 60, 1)
    es_visitante = vehiculo.es_visitante
    precio = (
        float(tarifa.precioHoraVisitante)
        if es_visitante and tarifa.precioHoraVisitante > 0
        else float(tarifa.precioHora)
    )
    return math.ceil((precio / 60) * total_minutos)
