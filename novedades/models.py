from django.db import models


class Novedad(models.Model):

    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En proceso'
        RESUELTO = 'RESUELTO', 'Resuelto'

    novDescripcion = models.TextField()
    novFoto = models.ImageField(upload_to='novedades/', blank=True, null=True)
    novEstado = models.CharField(
        max_length=10,
        choices=EstadoChoices.choices,
        default=EstadoChoices.PENDIENTE,
    )
    novComentario = models.TextField(blank=True)  # Acciones tomadas / seguimiento
    fkIdVehiculo = models.ForeignKey(
        'vehiculos.Vehiculo',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='novedades',
        db_column='fkIdVehiculo',
    )
    fkIdEspacio = models.ForeignKey(
        'parqueadero.Espacio',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='novedades',
        db_column='fkIdEspacio',
    )
    fkIdReportador = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        related_name='novedades_reportadas',
        db_column='fkIdReportador',
    )
    fkIdResponsable = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='novedades_asignadas',
        db_column='fkIdResponsable',
    )
    novFechaCreacion = models.DateTimeField(auto_now_add=True)
    novFechaActualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'novedades'
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'
        ordering = ['-novFechaCreacion']

    def __str__(self):
        return f'Novedad #{self.pk} — {self.get_novEstado_display()}'
