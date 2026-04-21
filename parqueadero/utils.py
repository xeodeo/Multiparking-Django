from datetime import datetime, timedelta

from django.utils import timezone

from pagos.models import Pago
from .models import Piso, InventarioParqueo


def _calcular_pisos_data(now):
    """
    Calcula estado de pisos/espacios para el dashboard (admin y guardia).
    Devuelve lista de objetos Piso con atributos INYECTADOS dinámicamente:
      piso.total_espacios, piso.ocupados_espacios, piso.ocupacion_pct, piso.espacios_list
      espacio.reserva_proxima, espacio.pago_pendiente, espacio.placa_actual

    ⚠ Tradeoff intencional: se inyectan atributos en los objetos ORM en lugar de usar
    un dataclass porque los templates de Django iteran directamente sobre estos objetos.
    Crear un DTO separado requeriría duplicar la lógica de template o usar un dict.
    Riesgo: estos atributos no aparecen en el modelo — un dev que imprima el modelo
    en otro contexto no los verá. No acceder a estos atributos fuera de esta función.
    """
    # 2 horas: ventana de tiempo para mostrar reservas "próximas" en el mapa de pisos.
    # Si la reserva está a más de 2h, no se marca visualmente; el guardia no necesita
    # anticiparse tanto. Cambiar aquí si el negocio quiere ampliar/reducir la ventana.
    limite_2h = now + timedelta(hours=2)
    pisos = Piso.objects.filter(pisEstado=True).prefetch_related(
        'espacios', 'espacios__reservas'
    ).order_by('pisNombre')

    pisos_list = []
    for piso in pisos:
        total_piso = piso.espacios.count()
        ocupados_piso = piso.espacios.filter(espEstado='OCUPADO').count()
        piso.ocupacion_pct = int((ocupados_piso / total_piso) * 100) if total_piso > 0 else 0
        piso.total_espacios = total_piso
        piso.ocupados_espacios = ocupados_piso

        espacios_list = []
        for espacio in piso.espacios.all():
            reserva_proxima = None
            pago_pendiente = False

            for reserva in espacio.reservas.filter(resEstado__in=['PENDIENTE', 'CONFIRMADA']):
                fhr = datetime.combine(reserva.resFechaReserva, reserva.resHoraInicio)
                fhr = timezone.make_aware(fhr)
                if now <= fhr <= limite_2h:
                    reserva_proxima = reserva
                    break

            espacio.placa_actual = None
            if espacio.espEstado == 'OCUPADO':
                pago_pendiente = Pago.objects.filter(
                    fkIdParqueo__fkIdEspacio=espacio,
                    fkIdParqueo__parHoraSalida__isnull=True,
                    pagEstado='PENDIENTE',
                    pagMetodo='EFECTIVO',
                ).exists()
                registro_activo = InventarioParqueo.objects.filter(
                    fkIdEspacio=espacio,
                    parHoraSalida__isnull=True
                ).select_related('fkIdVehiculo').first()
                if registro_activo:
                    espacio.placa_actual = registro_activo.fkIdVehiculo.vehPlaca

            espacio.reserva_proxima = reserva_proxima
            espacio.pago_pendiente = pago_pendiente
            espacios_list.append(espacio)

        piso.espacios_list = espacios_list
        pisos_list.append(piso)
    return pisos_list
