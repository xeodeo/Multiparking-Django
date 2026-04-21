from django.core.validators import MinValueValidator
from django.db import models


class Tarifa(models.Model):
    nombre = models.CharField(max_length=50)
    fkIdTipoEspacio = models.ForeignKey(
        'parqueadero.TipoEspacio',
        on_delete=models.CASCADE,
        related_name='tarifas',
        db_column='fkIdTipoEspacio',
    )
    precioHora = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    # Precio diferenciado para visitantes (sin cuenta registrada) — generalmente mayor que precioHora
    precioHoraVisitante = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    precioDia = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    precioMensual = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0, 'El precio no puede ser negativo')],
    )
    # Regla de negocio: solo debe existir UNA tarifa activa por TipoEspacio simultáneamente.
    # Esta restricción NO está en la base de datos (no hay unique_together con activa=True)
    # porque se necesita poder preparar una tarifa futura mientras la actual sigue activa,
    # y activarlas en un solo paso. La validación la hacen las vistas al activar/crear.
    # Riesgo: si se manipula directamente la BD o admin Django, pueden quedar 2 activas
    # y calcular_costo_parqueo() tomará la primera encontrada (orden no garantizado).
    activa = models.BooleanField(default=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField(null=True, blank=True)  # null = tarifa vigente indefinidamente

    class Meta:
        db_table = 'tarifas'
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'

    def __str__(self):
        return f'{self.nombre} - {self.fkIdTipoEspacio.nombre}'

    @classmethod
    def get_active_for(cls, tipo_espacio):
        """
        Retorna la tarifa activa para el tipo de espacio dado, o None.
        Centraliza la búsqueda para evitar duplicar el filtro en múltiples vistas.
        """
        return cls.objects.filter(fkIdTipoEspacio=tipo_espacio, activa=True).first()

    def precio_para(self, vehiculo):
        """
        Retorna el precio/hora correcto según el tipo de vehículo.
        Visitantes usan precioHoraVisitante cuando está configurado (> 0);
        si vale 0 se interpreta como "sin diferenciación" y se usa precioHora.
        """
        if vehiculo.es_visitante and self.precioHoraVisitante > 0:
            return float(self.precioHoraVisitante)
        return float(self.precioHora)

    def activar(self):
        """
        Activa esta tarifa y desactiva todas las otras del mismo TipoEspacio.
        Garantiza la regla de negocio: solo una tarifa activa por tipo a la vez.
        Usar este método en lugar de modificar .activa directamente.
        """
        Tarifa.objects.filter(
            fkIdTipoEspacio=self.fkIdTipoEspacio
        ).exclude(pk=self.pk).update(activa=False)
        self.activa = True
        self.save()
