# -*- coding: utf-8 -*-
"""
Script para generar datos de prueba en la base de datos local
Ejecutar: python generar_datos_prueba.py
"""
import os
import sys
import django
from datetime import timedelta

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
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
        'usuNombre': 'Cliente', 'usuApellido': 'de Prueba',
        'usuTelefono': '3001234567',
        'usuClaveHash': make_password('test123'),
        'rolTipoRol': 'CLIENTE',
        'usuEstado': True,
    }
)
print(f"[OK] Usuario: {usuario.usuNombre} {usuario.usuApellido} {'(creado)' if created else '(existente)'}")

# 2. Crear piso si no existe
piso, created = Piso.objects.get_or_create(
    pisNombre='Piso 1',
    defaults={'pisEstado': True}
)
print(f"[OK] Piso: {piso.pisNombre} {'(creado)' if created else '(existente)'}")

# 3. Crear tipos de espacio si no existen
tipo_carro, created = TipoEspacio.objects.get_or_create(nombre='Carro')
print(f"[OK] Tipo Espacio: Carro {'(creado)' if created else '(existente)'}")

tipo_moto, created = TipoEspacio.objects.get_or_create(nombre='Moto')
print(f"[OK] Tipo Espacio: Moto {'(creado)' if created else '(existente)'}")

# 4. Crear espacios si no existen
from datetime import date
espacios_creados = 0
for i in range(1, 4):  # 3 espacios de carro
    _, created = Espacio.objects.get_or_create(
        espNumero=f'C1-{i:02d}',
        defaults={
            'fkIdPiso': piso,
            'fkIdTipoEspacio': tipo_carro,
            'espEstado': 'DISPONIBLE',
        }
    )
    if created:
        espacios_creados += 1

for i in range(1, 3):  # 2 espacios de moto
    _, created = Espacio.objects.get_or_create(
        espNumero=f'M1-{i:02d}',
        defaults={
            'fkIdPiso': piso,
            'fkIdTipoEspacio': tipo_moto,
            'espEstado': 'DISPONIBLE',
        }
    )
    if created:
        espacios_creados += 1

print(f"[OK] Espacios: {espacios_creados} creados, {Espacio.objects.count()} totales")

# 5. Crear tarifas activas si no existen
tarifa, created = Tarifa.objects.get_or_create(
    fkIdTipoEspacio=tipo_carro,
    activa=True,
    defaults={
        'nombre': 'Tarifa Carros 2026',
        'precioHora': 5000,
        'precioHoraVisitante': 7000,
        'precioDia': 40000,
        'precioMensual': 450000,
        'fechaInicio': date.today(),
    }
)
print(f"[OK] Tarifa Carros: ${tarifa.precioHora}/h usuario | ${tarifa.precioHoraVisitante}/h visitante {'(creada)' if created else '(existente)'}")

Tarifa.objects.get_or_create(
    fkIdTipoEspacio=tipo_moto,
    activa=True,
    defaults={
        'nombre': 'Tarifa Motos 2026',
        'precioHora': 2000,
        'precioHoraVisitante': 3000,
        'precioDia': 18000,
        'precioMensual': 180000,
        'fechaInicio': date.today(),
    }
)
print(f"[OK] Tarifa Motos: $2,000/h usuario | $3,000/h visitante")

# 6. Crear vehículos de prueba si no existen
vehiculos = []
vehiculos_demo = [
    ('ABC123', 'Carro', 'Rojo', 'Toyota', 'Corolla'),
    ('DEF456', 'Carro', 'Blanco', 'Mazda', '3'),
    ('GHI789', 'Moto', 'Negro', 'Yamaha', 'FZ250'),
    ('JKL012', 'Carro', 'Gris', 'Chevrolet', 'Spark'),
    ('MNO345', 'Moto', 'Azul', 'Suzuki', 'GN125'),
]
for placa, tipo, color, marca, modelo in vehiculos_demo:
    vehiculo, created = Vehiculo.objects.get_or_create(
        vehPlaca=placa,
        defaults={
            'vehTipo': tipo,
            'vehColor': color,
            'vehMarca': marca,
            'vehModelo': modelo,
            'fkIdUsuario': usuario,
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

        # Calcular monto (3 horas * tarifa del tipo del vehiculo)
        tarifa_vehiculo = Tarifa.objects.filter(
            fkIdTipoEspacio=espacio.fkIdTipoEspacio, activa=True
        ).first() or tarifa
        monto = float(tarifa_vehiculo.precioHora) * 3

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
