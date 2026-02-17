# -*- coding: utf-8 -*-
"""
Script para cargar datos iniciales de forma automática
Se puede ejecutar después de las migraciones

Ejecutar: python cargar_datos_iniciales.py
"""
import os
import django
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from parqueadero.models import Piso, TipoEspacio, Espacio
from tarifas.models import Tarifa
from usuarios.models import Usuario
from vehiculos.models import Vehiculo
from datetime import date

print("=" * 60)
print(">> Cargando Datos Iniciales")
print("=" * 60)

# 1. Usuario admin (si no existe)
admin, created = Usuario.objects.get_or_create(
    usuCorreo='admin@multiparking.com',
    defaults={
        'usuDocumento': '0000000001',
        'usuNombreCompleto': 'Administrador',
        'usuTelefono': '3000000000',
        'usuClaveHash': make_password('admin123'),
        'rolTipoRol': 'ADMIN',
        'usuEstado': True,
    }
)
print(f"[OK] Admin: {admin.usuCorreo} {'(creado)' if created else '(existe)'}")

# 2. Usuario cliente demo
cliente, created = Usuario.objects.get_or_create(
    usuCorreo='cliente@test.com',
    defaults={
        'usuDocumento': '1234567890',
        'usuNombreCompleto': 'Cliente Demo',
        'usuTelefono': '3001234567',
        'usuClaveHash': make_password('test123'),
        'rolTipoRol': 'CLIENTE',
        'usuEstado': True,
    }
)
print(f"[OK] Cliente: {cliente.usuCorreo} {'(creado)' if created else '(existe)'}")

# 3. Pisos
for i in range(1, 4):
    piso, created = Piso.objects.get_or_create(
        pisNombre=f'Piso {i}',
        defaults={'pisEstado': True}
    )
    if created:
        print(f"[OK] Piso {i} creado")

# 4. Tipos de espacio
tipos = ['Estandar', 'Moto', 'VIP']

for nombre in tipos:
    tipo, created = TipoEspacio.objects.get_or_create(nombre=nombre)
    if created:
        print(f"[OK] Tipo: {nombre}")

# 5. Espacios
piso1 = Piso.objects.get(pisNombre='Piso 1')
tipo_std = TipoEspacio.objects.get(nombre='Estandar')
tipo_moto = TipoEspacio.objects.get(nombre='Moto')

for i in range(1, 21):  # 20 espacios estándar
    Espacio.objects.get_or_create(
        espNumero=f'A-{i:03d}',
        defaults={
            'fkIdPiso': piso1,
            'fkIdTipoEspacio': tipo_std,
            'espEstado': 'DISPONIBLE',
        }
    )

for i in range(1, 11):  # 10 espacios para motos
    Espacio.objects.get_or_create(
        espNumero=f'M-{i:03d}',
        defaults={
            'fkIdPiso': piso1,
            'fkIdTipoEspacio': tipo_moto,
            'espEstado': 'DISPONIBLE',
        }
    )

print(f"[OK] Espacios: {Espacio.objects.count()} totales")

# 6. Tarifas activas
# Verificar si ya existe una tarifa activa para cada tipo
if not Tarifa.objects.filter(fkIdTipoEspacio=tipo_std, activa=True).exists():
    Tarifa.objects.create(
        fkIdTipoEspacio=tipo_std,
        activa=True,
        nombre='Tarifa Estandar 2025',
        precioHora=5000,
        precioDia=50000,
        precioMensual=500000,
        fechaInicio=date.today(),
        fechaFin=None,
    )
    print("[OK] Tarifa Estandar creada")

if not Tarifa.objects.filter(fkIdTipoEspacio=tipo_moto, activa=True).exists():
    Tarifa.objects.create(
        fkIdTipoEspacio=tipo_moto,
        activa=True,
        nombre='Tarifa Motos 2025',
        precioHora=2000,
        precioDia=20000,
        precioMensual=200000,
        fechaInicio=date.today(),
        fechaFin=None,
    )
    print("[OK] Tarifa Motos creada")

print(f"[OK] Tarifas: {Tarifa.objects.filter(activa=True).count()} activas")

# 7. Vehículos de prueba
placas_demo = [
    ('ABC123', 'CARRO', 'Toyota', cliente),
    ('DEF456', 'CARRO', 'Mazda', cliente),
    ('GHI789', 'CARRO', 'Chevrolet', cliente),
    ('JKL012', 'MOTO', 'Yamaha', cliente),
    ('MNO345', 'MOTO', 'Suzuki', cliente),
]

for placa, tipo, marca, propietario in placas_demo:
    Vehiculo.objects.get_or_create(
        vehPlaca=placa,
        defaults={
            'vehTipo': tipo,
            'vehMarca': marca,
            'fkIdUsuario': propietario,
            'es_visitante': False,
        }
    )

print(f"[OK] Vehiculos: {Vehiculo.objects.count()} registrados")

print("\n" + "=" * 60)
print(">> DATOS INICIALES CARGADOS")
print("=" * 60)
print("\nAhora ejecuta: python mantener_datos_demo.py")
print("Para generar pagos de demostracion recientes")
