"""
Management command para enviar recordatorios de reservas 24 horas antes.

Uso:
    python manage.py enviar_recordatorios

En Render, configurar como Cron Job:
    Schedule: 0 13 * * *   (13:00 UTC = 8:00 AM Colombia/Bogotá)
    Command:  python manage.py enviar_recordatorios
"""
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from multiparking import email_utils
from reservas.models import Reserva


class Command(BaseCommand):
    help = 'Envía recordatorios por correo para las reservas del día siguiente'

    def handle(self, *args, **options):
        manana = date.today() + timedelta(days=1)

        # Buscar reservas activas (PENDIENTE o CONFIRMADA) para mañana
        reservas = Reserva.objects.filter(
            resFechaReserva=manana,
            resEstado__in=['PENDIENTE', 'CONFIRMADA']
        ).select_related(
            'fkIdVehiculo',
            'fkIdVehiculo__fkIdUsuario',
            'fkIdEspacio',
            'fkIdEspacio__fkIdPiso',
        )

        total = reservas.count()
        enviados = 0
        omitidos = 0

        self.stdout.write(f'Reservas para mañana ({manana}): {total}')

        for reserva in reservas:
            usuario = reserva.fkIdVehiculo.fkIdUsuario
            if not usuario:
                # Vehículo de visitante, sin correo asociado
                omitidos += 1
                continue

            email_utils.enviar_recordatorio_reserva(reserva)
            enviados += 1
            self.stdout.write(f'  ✓ Recordatorio enviado a {usuario.usuCorreo} — Reserva #{reserva.pk}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Completado: {enviados} enviados, {omitidos} omitidos (visitantes sin correo).'
            )
        )
