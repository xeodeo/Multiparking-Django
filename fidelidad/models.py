from django.db import models
from django.core.validators import MinValueValidator


class ConfiguracionFidelidad(models.Model):
    """Configuración global del sistema de stickers (singleton)."""
    metaStickers = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)],
        help_text='Número de stickers que un usuario necesita para reclamar el bono del 100%.'
    )
    diasVencimientoBono = models.PositiveIntegerField(
        default=30,
        help_text='Días de validez del cupón bono generado al canjear stickers.'
    )

    class Meta:
        db_table = 'fidelidad_configuracion'
        verbose_name = 'Configuración de Fidelidad'

    def save(self, *args, **kwargs):
        # Singleton: solo existe un registro
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f'Meta: {self.metaStickers} stickers | Bono: {self.diasVencimientoBono} días'


class Sticker(models.Model):
    """Un sticker ganado por un usuario al estar parqueado más de 1 hora."""
    fkIdUsuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='stickers',
        db_column='fkIdUsuario',
    )
    fkIdParqueo = models.OneToOneField(
        'parqueadero.InventarioParqueo',
        on_delete=models.CASCADE,
        related_name='sticker',
        db_column='fkIdParqueo',
    )
    stkFecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fidelidad_stickers'
        verbose_name = 'Sticker'
        verbose_name_plural = 'Stickers'

    def __str__(self):
        return f'Sticker de {self.fkIdUsuario} — {self.stkFecha:%Y-%m-%d}'
