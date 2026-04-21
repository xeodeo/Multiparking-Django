from django.core.validators import RegexValidator
from django.db import models


class Piso(models.Model):
    pisNombre = models.CharField(
        max_length=30,
        validators=[RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-]+$', 'El nombre solo acepta letras, números y guiones')],
    )
    pisEstado = models.BooleanField(default=True)  # True = activo, False = desactivado (ej. en mantenimiento)

    class Meta:
        db_table = 'pisos'
        verbose_name = 'Piso'
        verbose_name_plural = 'Pisos'

    def __str__(self):
        return self.pisNombre


class TipoEspacio(models.Model):
    # Categoría del espacio: 'Carro' o 'Moto' — determina qué tarifa aplica
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'tipos_espacio'
        verbose_name = 'Tipo de Espacio'
        verbose_name_plural = 'Tipos de Espacio'

    def __str__(self):
        return self.nombre


class Espacio(models.Model):

    class EstadoChoices(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'  # Libre para recibir vehículos
        OCUPADO = 'OCUPADO', 'Ocupado'            # Hay un vehículo estacionado
        RESERVADO = 'RESERVADO', 'Reservado'      # Bloqueado por una reserva activa
        INACTIVO = 'INACTIVO', 'Inactivo'         # Fuera de servicio (mantenimiento, etc.)

    espNumero = models.CharField(max_length=10)  # Código único del puesto, ej. 'C1-01', 'M2-05'
    fkIdPiso = models.ForeignKey(
        Piso,
        on_delete=models.CASCADE,
        related_name='espacios',
        db_column='fkIdPiso',
    )
    fkIdTipoEspacio = models.ForeignKey(
        TipoEspacio,
        on_delete=models.CASCADE,
        related_name='espacios',
        db_column='fkIdTipoEspacio',
    )
    # Regla de integridad de estados:
    # DISPONIBLE → puede recibir un vehículo (ingreso normal o desde reserva)
    # OCUPADO    → hay un InventarioParqueo activo (parHoraSalida IS NULL) para este espacio
    # RESERVADO  → hay una Reserva PENDIENTE o CONFIRMADA; el espacio está bloqueado
    # INACTIVO   → fuera de servicio; las vistas lo excluyen de todos los flujos operativos
    # Transición correcta: DISPONIBLE → RESERVADO → OCUPADO → DISPONIBLE
    # Si se cancela la reserva antes del ingreso: RESERVADO → DISPONIBLE (Reserva.cerrar())
    espEstado = models.CharField(
        max_length=10,
        choices=EstadoChoices.choices,
        default=EstadoChoices.DISPONIBLE,
    )

    class Meta:
        db_table = 'espacios'
        verbose_name = 'Espacio'
        verbose_name_plural = 'Espacios'
        unique_together = [('fkIdPiso', 'espNumero')]  # El mismo número no puede repetirse dentro de un piso
        indexes = [
            models.Index(fields=['espNumero'], name='idx_espacio_numero'),
        ]

    def __str__(self):
        return f'{self.espNumero} - Piso {self.fkIdPiso}'

    def ocupar(self):
        """Marca el espacio como OCUPADO y guarda solo ese campo."""
        self.espEstado = 'OCUPADO'
        self.save(update_fields=['espEstado'])

    def liberar(self):
        """Marca el espacio como DISPONIBLE y guarda solo ese campo."""
        self.espEstado = 'DISPONIBLE'
        self.save(update_fields=['espEstado'])

    def reservar(self):
        """Marca el espacio como RESERVADO y guarda solo ese campo."""
        self.espEstado = 'RESERVADO'
        self.save(update_fields=['espEstado'])


class InventarioParqueo(models.Model):
    parHoraEntrada = models.DateTimeField(auto_now_add=True)              # Se asigna automáticamente al crear el registro
    # parHoraSalida NULL significa "vehículo todavía estacionado".
    # NO existe un campo 'estado'; la presencia/ausencia de este valor ES el estado.
    # Consecuencia: para saber si un espacio está ocupado, siempre filtrar por
    # parHoraSalida__isnull=True, nunca por un string de estado en esta tabla.
    parHoraSalida = models.DateTimeField(null=True, blank=True)            # NULL = vehículo aún estacionado; con valor = ya salió
    fkIdVehiculo = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.CASCADE,
        related_name='parqueos',
        db_column='fkIdVehiculo',
    )
    fkIdEspacio = models.ForeignKey(
        Espacio,
        on_delete=models.CASCADE,
        related_name='parqueos',
        db_column='fkIdEspacio',
    )

    class Meta:
        db_table = 'inventario_parqueo'
        verbose_name = 'Inventario Parqueo'
        verbose_name_plural = 'Inventario Parqueo'
        indexes = [
            # Índice parcial conceptual: la query más frecuente del sistema es
            # "¿qué vehículos están actualmente parqueados?" = parHoraSalida IS NULL.
            # Sin este índice, cada carga del dashboard hace un full-scan de toda
            # la tabla de registros históricos.
            models.Index(fields=['parHoraSalida'], name='idx_parqueo_estado'),
        ]

    def __str__(self):
        estado = 'Activo' if self.parHoraSalida is None else 'Finalizado'
        return f'{self.fkIdVehiculo.vehPlaca} - {estado}'

    def duracion_str(self, ahora=None) -> str:
        """
        Retorna la duración del turno formateada: '1d 2h 30m'.
        ahora=None → usa timezone.now() para turnos activos (sin parHoraSalida).
        """
        from django.utils import timezone
        fin = ahora or self.parHoraSalida or timezone.now()
        # Misma fórmula +59 que calcular_costo_parqueo: garantiza mínimo 1 minuto
        total_min = max((int((fin - self.parHoraEntrada).total_seconds()) + 59) // 60, 1)
        d, resto = divmod(total_min, 1440)
        h, m = divmod(resto, 60)
        partes = []
        if d:
            partes.append(f'{d}d')
        if h:
            partes.append(f'{h}h')
        partes.append(f'{m}m')
        return ' '.join(partes)
