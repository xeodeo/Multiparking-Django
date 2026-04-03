from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parqueadero', '0001_initial'),
        ('usuarios', '0001_initial'),
        ('vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('novDescripcion', models.TextField()),
                ('novFoto', models.ImageField(blank=True, null=True, upload_to='novedades/')),
                ('novEstado', models.CharField(
                    choices=[('PENDIENTE', 'Pendiente'), ('EN_PROCESO', 'En proceso'), ('RESUELTO', 'Resuelto')],
                    default='PENDIENTE',
                    max_length=10,
                )),
                ('novComentario', models.TextField(blank=True)),
                ('novFechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('novFechaActualizacion', models.DateTimeField(auto_now=True)),
                ('fkIdVehiculo', models.ForeignKey(
                    blank=True, db_column='fkIdVehiculo', null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='novedades', to='vehiculos.vehiculo',
                )),
                ('fkIdEspacio', models.ForeignKey(
                    blank=True, db_column='fkIdEspacio', null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='novedades', to='parqueadero.espacio',
                )),
                ('fkIdReportador', models.ForeignKey(
                    db_column='fkIdReportador', null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='novedades_reportadas', to='usuarios.usuario',
                )),
                ('fkIdResponsable', models.ForeignKey(
                    blank=True, db_column='fkIdResponsable', null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='novedades_asignadas', to='usuarios.usuario',
                )),
            ],
            options={
                'verbose_name': 'Novedad',
                'verbose_name_plural': 'Novedades',
                'db_table': 'novedades',
                'ordering': ['-novFechaCreacion'],
            },
        ),
    ]
