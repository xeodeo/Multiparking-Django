from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parqueadero', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionFidelidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metaStickers', models.PositiveIntegerField(
                    default=10,
                    help_text='Número de stickers que un usuario necesita para reclamar el bono del 100%.',
                    validators=[django.core.validators.MinValueValidator(1)],
                )),
                ('diasVencimientoBono', models.PositiveIntegerField(
                    default=30,
                    help_text='Días de validez del cupón bono generado al canjear stickers.',
                )),
            ],
            options={
                'verbose_name': 'Configuración de Fidelidad',
                'db_table': 'fidelidad_configuracion',
            },
        ),
        migrations.CreateModel(
            name='Sticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stkFecha', models.DateTimeField(auto_now_add=True)),
                ('fkIdUsuario', models.ForeignKey(
                    db_column='fkIdUsuario',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='stickers',
                    to='usuarios.usuario',
                )),
                ('fkIdParqueo', models.OneToOneField(
                    db_column='fkIdParqueo',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sticker',
                    to='parqueadero.inventarioparqueo',
                )),
            ],
            options={
                'verbose_name': 'Sticker',
                'verbose_name_plural': 'Stickers',
                'db_table': 'fidelidad_stickers',
            },
        ),
    ]
