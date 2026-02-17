# -*- coding: utf-8 -*-
"""
Script para mantener datos de demostración siempre actualizados
Este script se puede ejecutar diariamente para asegurar que siempre
haya datos de pagos en los últimos 7 días.

Ejecutar: python mantener_datos_demo.py
"""
import os
import django
from datetime import timedelta
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from django.utils import timezone
from parqueadero.models import Espacio, InventarioParqueo
from vehiculos.models import Vehiculo
from tarifas.models import Tarifa
from pagos.models import Pago
from usuarios.models import Usuario

print("=" * 60)
print(">> Mantenimiento de Datos de Demostracion")
print("=" * 60)

# Verificar datos necesarios
now = timezone.now()
hoy_local = timezone.localtime(now).date()
hace_7_dias = hoy_local - timedelta(days=6)

# 1. Verificar pagos recientes
from datetime import datetime
inicio_rango = timezone.make_aware(datetime.combine(hace_7_dias, datetime.min.time()))
fin_rango = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))

pagos_recientes = Pago.objects.filter(
    pagFechaPago__range=(inicio_rango, fin_rango),
    pagEstado='PAGADO',
)

print(f"\n[INFO] Fecha actual: {hoy_local}")
print(f"[INFO] Rango de busqueda: {hace_7_dias} a {hoy_local}")
print(f"[INFO] Pagos en ultimos 7 dias: {pagos_recientes.count()}")

# 2. Si hay menos de 14 pagos, generar más
if pagos_recientes.count() < 14:
    print(f"\n[ACCION] Generando nuevos pagos para mantener datos de demo...")

    # Obtener datos necesarios
    usuario = Usuario.objects.filter(rolTipoRol='CLIENTE').first()
    vehiculos = list(Vehiculo.objects.all()[:5])
    tarifa = Tarifa.objects.filter(activa=True).first()

    if not usuario or not vehiculos or not tarifa:
        print("[ERROR] Faltan datos basicos. Ejecuta primero: python generar_datos_prueba.py")
        sys.exit(1)

    pagos_creados = 0

    # Generar 3 pagos por día para los últimos 5 días
    for dia_offset in range(5):
        # Usar fecha local para el día
        dia_fecha = hoy_local - timedelta(days=dia_offset)

        for i in range(3):
            # Seleccionar vehículo
            vehiculo = vehiculos[i % len(vehiculos)]
            espacio = Espacio.objects.filter(espEstado='DISPONIBLE').first()

            if not espacio:
                espacio = Espacio.objects.first()
                if espacio:
                    espacio.espEstado = 'DISPONIBLE'
                    espacio.save()

            if not espacio:
                print("[ERROR] No hay espacios disponibles")
                break

            # Crear datetime aware para este día a las 10am-5pm local
            from datetime import datetime
            hora_base = 10 + (i * 2)  # 10am, 12pm, 2pm

            # Crear datetime naive y luego convertir a aware con zona horaria del proyecto
            hora_entrada_naive = datetime(dia_fecha.year, dia_fecha.month, dia_fecha.day, hora_base, 0, 0)
            hora_salida_naive = datetime(dia_fecha.year, dia_fecha.month, dia_fecha.day, hora_base + 3, 0, 0)

            # make_aware usa la timezone del proyecto (America/Bogota) por defecto
            hora_entrada_dt = timezone.make_aware(hora_entrada_naive)
            hora_salida_dt = timezone.make_aware(hora_salida_naive)

            # Crear registro de inventario
            # Nota: parHoraEntrada tiene auto_now_add=True, así que debemos actualizar después
            registro = InventarioParqueo.objects.create(
                fkIdVehiculo=vehiculo,
                fkIdEspacio=espacio,
                parHoraSalida=hora_salida_dt,
            )
            # Actualizar la hora de entrada manualmente para datos de prueba
            InventarioParqueo.objects.filter(pk=registro.pk).update(
                parHoraEntrada=hora_entrada_dt
            )

            # Calcular monto (3 horas * tarifa)
            horas = 3
            monto = float(tarifa.precioHora) * horas

            # Crear pago
            # Nota: pagFechaPago también tiene auto_now_add=True
            pago = Pago.objects.create(
                pagMonto=monto,
                pagMetodo='EFECTIVO',
                pagEstado='PAGADO',
                fkIdParqueo=registro,
            )
            # Actualizar la fecha del pago manualmente para datos de prueba
            Pago.objects.filter(pk=pago.pk).update(pagFechaPago=hora_salida_dt)
            pagos_creados += 1

    print(f"[OK] Se crearon {pagos_creados} nuevos pagos")
else:
    print("\n[OK] Hay suficientes pagos recientes. No se requiere accion.")

# 3. Limpiar pagos muy antiguos (más de 30 días)
hace_30_dias = hoy_local - timedelta(days=30)
pagos_antiguos = Pago.objects.filter(
    pagFechaPago__date__lt=hace_30_dias,
    pagMetodo='EFECTIVO',  # Solo borrar datos de prueba
)
num_antiguos = pagos_antiguos.count()

if num_antiguos > 0:
    print(f"\n[INFO] Limpiando {num_antiguos} pagos antiguos (mas de 30 dias)...")
    # Obtener IDs de inventario para borrar también
    inventario_ids = list(pagos_antiguos.values_list('fkIdParqueo', flat=True))
    pagos_antiguos.delete()
    InventarioParqueo.objects.filter(pk__in=inventario_ids).delete()
    print(f"[OK] Pagos antiguos eliminados")

# 4. Resumen final
print("\n" + "=" * 60)
print(">> RESUMEN")
print("=" * 60)

pagos_actuales = Pago.objects.filter(
    pagFechaPago__range=(inicio_rango, fin_rango),
    pagEstado='PAGADO',
)

print(f"Pagos en ultimos 7 dias: {pagos_actuales.count()}")
print(f"Total pagos en sistema: {Pago.objects.count()}")
print(f"Total inventario: {InventarioParqueo.objects.count()}")

if pagos_actuales.count() > 0:
    total_ingresos = sum([float(p.pagMonto) for p in pagos_actuales])
    print(f"Ingresos ultimos 7 dias: ${total_ingresos:,.0f}")

    # Mostrar distribución por día
    print("\nDistribucion por dia:")
    for dia_offset in range(7):
        dia = hoy_local - timedelta(days=dia_offset)
        dia_inicio = timezone.make_aware(datetime.combine(dia, datetime.min.time()))
        dia_fin = timezone.make_aware(datetime.combine(dia, datetime.max.time()))
        pagos_dia = pagos_actuales.filter(pagFechaPago__range=(dia_inicio, dia_fin))
        if pagos_dia.count() > 0:
            total_dia = sum([float(p.pagMonto) for p in pagos_dia])
            print(f"  {dia}: {pagos_dia.count()} pagos - ${total_dia:,.0f}")

print("\n[OK] Mantenimiento completado!")
print("Recarga el dashboard para ver los datos actualizados:")
print("URL: http://127.0.0.1:8000/admin-panel/")
