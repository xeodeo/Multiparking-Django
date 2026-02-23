# -*- coding: utf-8 -*-
"""
Script para cargar datos iniciales de forma automática
Se puede ejecutar después de las migraciones

Ejecutar: python scripts/cargar_datos_iniciales.py
"""
import os
import django
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configurar path al proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from parqueadero.models import Piso, TipoEspacio, Espacio
from tarifas.models import Tarifa
from usuarios.models import Usuario
from vehiculos.models import Vehiculo
from cupones.models import Cupon
from datetime import date, timedelta

print("=" * 60)
print(">> Cargando Datos Iniciales - Multiparking")
print("=" * 60)

# ── 1. USUARIOS ──────────────────────────────────────────────
print("\n[1/8] Creando usuarios...")

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
print(f"  [OK] Admin: admin@multiparking.com / admin123 {'(creado)' if created else '(existe)'}")

vigilante, created = Usuario.objects.get_or_create(
    usuCorreo='vigilante@multiparking.com',
    defaults={
        'usuDocumento': '0000000002',
        'usuNombreCompleto': 'Vigilante Principal',
        'usuTelefono': '3001111111',
        'usuClaveHash': make_password('vigil123'),
        'rolTipoRol': 'VIGILANTE',
        'usuEstado': True,
    }
)
print(f"  [OK] Vigilante: vigilante@multiparking.com / vigil123 {'(creado)' if created else '(existe)'}")

cliente, created = Usuario.objects.get_or_create(
    usuCorreo='cliente@test.com',
    defaults={
        'usuDocumento': '1234567890',
        'usuNombreCompleto': 'Carlos Perez',
        'usuTelefono': '3001234567',
        'usuClaveHash': make_password('test123'),
        'rolTipoRol': 'CLIENTE',
        'usuEstado': True,
    }
)
print(f"  [OK] Cliente: cliente@test.com / test123 {'(creado)' if created else '(existe)'}")

cliente2, created = Usuario.objects.get_or_create(
    usuCorreo='maria@test.com',
    defaults={
        'usuDocumento': '9876543210',
        'usuNombreCompleto': 'Maria Lopez',
        'usuTelefono': '3009876543',
        'usuClaveHash': make_password('test123'),
        'rolTipoRol': 'CLIENTE',
        'usuEstado': True,
    }
)
print(f"  [OK] Cliente 2: maria@test.com / test123 {'(creado)' if created else '(existe)'}")

# ── 2. TIPOS DE ESPACIO (Solo Carro y Moto) ─────────────────
print("\n[2/8] Creando tipos de espacio...")

tipo_carro, created = TipoEspacio.objects.get_or_create(nombre='Carro')
print(f"  [OK] Tipo: Carro {'(creado)' if created else '(existe)'}")

tipo_moto, created = TipoEspacio.objects.get_or_create(nombre='Moto')
print(f"  [OK] Tipo: Moto {'(creado)' if created else '(existe)'}")

# Desactivar tipos que no se usan (solo si no tienen espacios asignados)
for nombre_tipo in ['VIP', 'Visitante', 'Estandar']:
    tipo_viejo = TipoEspacio.objects.filter(nombre=nombre_tipo).first()
    if tipo_viejo and not tipo_viejo.espacios.exists():
        tipo_viejo.delete()
        print(f"  [OK] Tipo '{nombre_tipo}' eliminado (sin espacios)")

# ── 3. PISOS ─────────────────────────────────────────────────
print("\n[3/8] Creando pisos...")

pisos_config = [
    ('Piso 1 - Subsuelo', True),
    ('Piso 2 - Nivel Calle', True),
    ('Piso 3 - Terraza', True),
]

pisos = []
for nombre, estado in pisos_config:
    piso, created = Piso.objects.get_or_create(
        pisNombre=nombre,
        defaults={'pisEstado': estado}
    )
    pisos.append(piso)
    print(f"  [OK] {nombre} {'(creado)' if created else '(existe)'}")

# ── 4. ESPACIOS ──────────────────────────────────────────────
print("\n[4/8] Creando espacios...")

espacios_config = [
    # (piso_index, prefijo, tipo, cantidad)
    (0, 'C1', tipo_carro, 15),   # Piso 1: 15 carros
    (0, 'M1', tipo_moto, 10),    # Piso 1: 10 motos
    (1, 'C2', tipo_carro, 20),   # Piso 2: 20 carros
    (1, 'M2', tipo_moto, 8),     # Piso 2: 8 motos
    (2, 'C3', tipo_carro, 12),   # Piso 3: 12 carros
    (2, 'M3', tipo_moto, 6),     # Piso 3: 6 motos
]

total_creados = 0
for piso_idx, prefijo, tipo, cantidad in espacios_config:
    for i in range(1, cantidad + 1):
        _, created = Espacio.objects.get_or_create(
            espNumero=f'{prefijo}-{i:02d}',
            defaults={
                'fkIdPiso': pisos[piso_idx],
                'fkIdTipoEspacio': tipo,
                'espEstado': 'DISPONIBLE',
            }
        )
        if created:
            total_creados += 1

print(f"  [OK] {total_creados} espacios nuevos creados")
print(f"  [OK] Total espacios: {Espacio.objects.count()}")
print(f"       Carros: {Espacio.objects.filter(fkIdTipoEspacio=tipo_carro).count()}")
print(f"       Motos:  {Espacio.objects.filter(fkIdTipoEspacio=tipo_moto).count()}")

# ── 5. TARIFAS ───────────────────────────────────────────────
print("\n[5/8] Creando tarifas...")

# Tarifa Carros
tarifa_carro, created = Tarifa.objects.get_or_create(
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
if not created:
    tarifa_carro.precioHoraVisitante = 7000
    tarifa_carro.save()
print(f"  [OK] Tarifa Carros: $5,000/h usuario | $7,000/h visitante {'(creado)' if created else '(actualizado)'}")

# Tarifa Motos
tarifa_moto, created = Tarifa.objects.get_or_create(
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
if not created:
    tarifa_moto.precioHoraVisitante = 3000
    tarifa_moto.save()
print(f"  [OK] Tarifa Motos: $2,000/h usuario | $3,000/h visitante {'(creado)' if created else '(actualizado)'}")

# ── 6. VEHICULOS DE PRUEBA ───────────────────────────────────
print("\n[6/8] Creando vehiculos de prueba...")

vehiculos_demo = [
    ('ABC123', 'CARRO', 'Rojo', 'Toyota', 'Corolla', cliente),
    ('DEF456', 'CARRO', 'Blanco', 'Mazda', '3', cliente),
    ('JKL012', 'MOTO', 'Negro', 'Yamaha', 'FZ250', cliente),
    ('MNO345', 'CARRO', 'Gris', 'Chevrolet', 'Spark', cliente2),
    ('PQR678', 'MOTO', 'Azul', 'Suzuki', 'GN125', cliente2),
]

for placa, tipo, color, marca, modelo, propietario in vehiculos_demo:
    _, created = Vehiculo.objects.get_or_create(
        vehPlaca=placa,
        defaults={
            'vehTipo': tipo,
            'vehColor': color,
            'vehMarca': marca,
            'vehModelo': modelo,
            'fkIdUsuario': propietario,
            'es_visitante': False,
        }
    )
    if created:
        print(f"  [OK] {placa} - {marca} {modelo} ({tipo})")

print(f"  [OK] Total vehiculos: {Vehiculo.objects.count()}")

# ── 7. CUPONES DE DESCUENTO ──────────────────────────────────
print("\n[7/8] Creando cupones de descuento...")

hoy = date.today()
cupones_demo = [
    {
        'cupNombre': 'Descuento Bienvenida',
        'cupCodigo': 'BIENVENIDO20',
        'cupTipo': 'PORCENTAJE',
        'cupValor': 20,
        'cupDescripcion': '20% de descuento para nuevos usuarios',
        'cupFechaInicio': hoy,
        'cupFechaFin': hoy + timedelta(days=90),
    },
    {
        'cupNombre': 'Descuento Fijo $5,000',
        'cupCodigo': 'DESCUENTO5K',
        'cupTipo': 'VALOR_FIJO',
        'cupValor': 5000,
        'cupDescripcion': '$5,000 de descuento directo en tu pago',
        'cupFechaInicio': hoy,
        'cupFechaFin': hoy + timedelta(days=60),
    },
    {
        'cupNombre': 'Promo Fin de Semana',
        'cupCodigo': 'FINDE50',
        'cupTipo': 'PORCENTAJE',
        'cupValor': 50,
        'cupDescripcion': '50% de descuento los fines de semana',
        'cupFechaInicio': hoy,
        'cupFechaFin': hoy + timedelta(days=30),
    },
]

for cupon_data in cupones_demo:
    _, created = Cupon.objects.get_or_create(
        cupCodigo=cupon_data['cupCodigo'],
        defaults=cupon_data
    )
    if created:
        print(f"  [OK] '{cupon_data['cupNombre']}' -> Codigo: {cupon_data['cupCodigo']}")
    else:
        print(f"  [--] '{cupon_data['cupCodigo']}' ya existe")

# ── 8. RESUMEN ───────────────────────────────────────────────
print("\n" + "=" * 60)
print(">> DATOS INICIALES CARGADOS EXITOSAMENTE")
print("=" * 60)
print(f"""
  Usuarios:  {Usuario.objects.count()}
  Pisos:     {Piso.objects.filter(pisEstado=True).count()}
  Espacios:  {Espacio.objects.count()} (Carros: {Espacio.objects.filter(fkIdTipoEspacio=tipo_carro).count()}, Motos: {Espacio.objects.filter(fkIdTipoEspacio=tipo_moto).count()})
  Tarifas:   {Tarifa.objects.filter(activa=True).count()} activas
  Vehiculos: {Vehiculo.objects.count()}
  Cupones:   {Cupon.objects.filter(cupActivo=True).count()} activos

  Credenciales:
    Admin:     admin@multiparking.com / admin123
    Vigilante: vigilante@multiparking.com / vigil123
    Cliente 1: cliente@test.com / test123
    Cliente 2: maria@test.com / test123

  Codigos de cupon:
    BIENVENIDO20  -> 20% descuento
    DESCUENTO5K   -> $5,000 de descuento
    FINDE50       -> 50% descuento
""")
