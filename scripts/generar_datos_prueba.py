# -*- coding: utf-8 -*-
"""
Script para generar datos de prueba en la base de datos local
Ejecutar: python generar_datos_prueba.py
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
from django.contrib.auth.hashers import make_password
from parqueadero.models import Piso, TipoEspacio, Espacio, InventarioParqueo
from vehiculos.models import Vehiculo
from tarifas.models import Tarifa
from pagos.models import Pago
from usuarios.models import Usuario

print(">> Generando datos de prueba para MultiParking...")
print("=" * 60)

# 1. Crear usuario de prueba si no existe
usuario, created = Usuario.objects.get_or_create(
    usuCorreo='cliente@test.com',
    defaults={
        'usuDocumento': '1234567890',
        'usuNombreCompleto': 'Cliente de Prueba',
        'usuTelefono': '3001234567',
        'usuClaveHash': make_password('test123'),
        'rolTipoRol': 'CLIENTE',
        'usuEstado': True,
    }
)
print(f"[OK] Usuario: {usuario.usuNombreCompleto} {'(creado)' if created else '(existente)'}")

# 2. Crear piso si no existe
piso, created = Piso.objects.get_or_create(
    pisNombre='Piso 1',
    defaults={'pisEstado': True}
)
print(f"[OK] Piso: {piso.pisNombre} {'(creado)' if created else '(existente)'}")

# 3. Crear tipo de espacio si no existe
tipo_espacio, created = TipoEspacio.objects.get_or_create(
    nombre='Estandar',
)
print(f"[OK] Tipo Espacio: {tipo_espacio.nombre} {'(creado)' if created else '(existente)'}")

# 4. Crear espacios si no existen
espacios_creados = 0
for i in range(1, 6):  # Crear 5 espacios
    espacio, created = Espacio.objects.get_or_create(
        espNumero=f'A-{i:03d}',
        defaults={
            'fkIdPiso': piso,
            'fkIdTipoEspacio': tipo_espacio,
            'espEstado': 'DISPONIBLE',
        }
    )
    if created:
        espacios_creados += 1
print(f"[OK] Espacios: {espacios_creados} creados, {Espacio.objects.count()} totales")

# 5. Crear tarifa activa si no existe
from datetime import date
tarifa, created = Tarifa.objects.get_or_create(
    fkIdTipoEspacio=tipo_espacio,
    activa=True,
    defaults={
        'nombre': 'Tarifa Estandar 2024',
        'precioHora': 5000,
        'precioDia': 50000,
        'precioMensual': 500000,
        'fechaInicio': date.today(),
        'fechaFin': None,
    }
)
print(f"[OK] Tarifa: ${tarifa.precioHora}/hora {'(creada)' if created else '(existente)'}")

# 6. Crear vehículos de prueba si no existen
vehiculos = []
placas = ['ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345']
for placa in placas:
    vehiculo, created = Vehiculo.objects.get_or_create(
        vehPlaca=placa,
        defaults={
            'vehTipo': 'CARRO',
            'vehMarca': 'Toyota',
            'fkIdUsuario': usuario,
            'es_visitante': False,
        }
    )
    vehiculos.append(vehiculo)
print(f"[OK] Vehiculos: {len(vehiculos)} vehiculos de prueba")

# 7. Generar pagos de los últimos 7 días
print("\n>> Generando pagos de prueba (ultimos 7 dias)...")
now = timezone.now()
pagos_creados = 0

# NO borrar pagos anteriores - queremos datos persistentes
# Verificar si ya existen pagos recientes
hoy_local = timezone.localtime(now).date()
hace_7_dias = hoy_local - timedelta(days=6)
pagos_recientes = Pago.objects.filter(
    pagFechaPago__date__gte=hace_7_dias,
    pagFechaPago__date__lte=hoy_local,
    pagEstado='PAGADO',
).count()

print(f"[INFO] Pagos existentes en ultimos 7 dias: {pagos_recientes}")

if pagos_recientes >= 15:
    print("[INFO] Ya hay suficientes pagos recientes. Saltando generacion.")
    pagos_creados = 0
else:
    print(f"[INFO] Generando mas pagos para completar datos de demostracion...")

for dia_offset in range(7):  # Últimos 7 días
    if pagos_recientes >= 15:
        break
    dia = now - timedelta(days=dia_offset)

    # Crear 2-4 pagos por día
    num_pagos = 2 + (dia_offset % 3)  # Varía entre 2 y 4

    for i in range(num_pagos):
        # Seleccionar vehículo y espacio
        vehiculo = vehiculos[i % len(vehiculos)]
        espacio = Espacio.objects.filter(espEstado='DISPONIBLE').first()

        if not espacio:
            # Si no hay espacios disponibles, liberar uno
            espacio = Espacio.objects.first()
            espacio.espEstado = 'DISPONIBLE'
            espacio.save()

        # Simular entrada hace algunas horas
        hora_entrada = dia - timedelta(hours=3 + i)
        hora_salida = dia - timedelta(hours=i)

        # Crear registro de inventario
        # Nota: parHoraEntrada tiene auto_now_add=True
        registro = InventarioParqueo.objects.create(
            fkIdVehiculo=vehiculo,
            fkIdEspacio=espacio,
            parHoraSalida=hora_salida,
        )
        # Actualizar manualmente para datos de prueba
        InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada)

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
        # Actualizar manualmente para datos de prueba
        Pago.objects.filter(pk=pago.pk).update(pagFechaPago=hora_salida)
        pagos_creados += 1

print(f"[OK] Pagos creados: {pagos_creados}")

# 8. Resumen
print("\n" + "=" * 60)
print(">> DATOS DE PRUEBA GENERADOS EXITOSAMENTE")
print("=" * 60)
print(f"Usuarios: {Usuario.objects.count()}")
print(f"Pisos: {Piso.objects.count()}")
print(f"Tipos de Espacio: {TipoEspacio.objects.count()}")
print(f"Espacios: {Espacio.objects.count()}")
print(f"Tarifas: {Tarifa.objects.count()}")
print(f"Vehiculos: {Vehiculo.objects.count()}")
print(f"Pagos: {Pago.objects.count()}")
print(f"Inventario: {InventarioParqueo.objects.count()}")

# Calcular total de ingresos
total_ingresos = sum([float(p.pagMonto) for p in Pago.objects.filter(pagEstado='PAGADO')])
print(f"\nTotal ingresos: ${total_ingresos:,.0f}")

print("\n>> Ahora recarga el dashboard para ver la grafica con datos!")
print("URL: http://127.0.0.1:8000/admin-panel/")
