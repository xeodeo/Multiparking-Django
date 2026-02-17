# -*- coding: utf-8 -*-
"""
Script para limpiar y regenerar la base de datos con datos específicos
Ejecutar: python reiniciar_base_datos.py
"""
import os
import django
import sys
from datetime import date, timedelta, datetime

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
from cupones.models import Cupon, CuponAplicado
from reservas.models import Reserva
from usuarios.models import Usuario

print("=" * 60)
print(">> LIMPIANDO Y REGENERANDO BASE DE DATOS")
print("=" * 60)

# 1. LIMPIAR TODO
print("\n[1/7] Limpiando base de datos...")
CuponAplicado.objects.all().delete()
Cupon.objects.all().delete()
Reserva.objects.all().delete()
Pago.objects.all().delete()
InventarioParqueo.objects.all().delete()
Espacio.objects.all().delete()
Tarifa.objects.all().delete()
TipoEspacio.objects.all().delete()
Piso.objects.all().delete()
Vehiculo.objects.all().delete()
Usuario.objects.all().delete()
print("[OK] Base de datos limpiada")

# 2. CREAR USUARIOS
print("\n[2/7] Creando usuarios...")
admin = Usuario.objects.create(
    usuCorreo='admin@multiparking.com',
    usuDocumento='0000000001',
    usuNombreCompleto='Administrador Principal',
    usuTelefono='3000000000',
    usuClaveHash=make_password('admin123'),
    rolTipoRol='ADMIN',
    usuEstado=True,
)
print(f"[OK] Admin: {admin.usuCorreo}")

cliente = Usuario.objects.create(
    usuCorreo='cliente@test.com',
    usuDocumento='1234567890',
    usuNombreCompleto='Cliente de Prueba',
    usuTelefono='3001234567',
    usuClaveHash=make_password('test123'),
    rolTipoRol='CLIENTE',
    usuEstado=True,
)
print(f"[OK] Cliente: {cliente.usuCorreo}")

vigilante = Usuario.objects.create(
    usuCorreo='vigilante@multiparking.com',
    usuDocumento='9876543210',
    usuNombreCompleto='Vigilante Principal',
    usuTelefono='3009876543',
    usuClaveHash=make_password('vigilante123'),
    rolTipoRol='VIGILANTE',
    usuEstado=True,
)
print(f"[OK] Vigilante: {vigilante.usuCorreo}")

# 3. CREAR PISOS (4 pisos, 1 desactivado)
print("\n[3/7] Creando pisos...")
pisos = []
for i in range(1, 5):
    piso = Piso.objects.create(
        pisNombre=f'Piso {i}',
        pisEstado=(i != 4)  # Piso 4 desactivado
    )
    pisos.append(piso)
    estado_txt = "activo" if piso.pisEstado else "DESACTIVADO"
    print(f"[OK] {piso.pisNombre} ({estado_txt})")

# 4. CREAR TIPOS DE ESPACIO
print("\n[4/7] Creando tipos de espacio...")
tipo_estandar = TipoEspacio.objects.create(nombre='Estandar')
tipo_moto = TipoEspacio.objects.create(nombre='Moto')
tipo_vip = TipoEspacio.objects.create(nombre='VIP')
print(f"[OK] Tipos: Estandar, Moto, VIP")

# 5. CREAR TARIFAS (2 por tipo, 1 activa y 1 desactivada)
print("\n[5/7] Creando tarifas...")

# Tarifas Estándar
Tarifa.objects.create(
    fkIdTipoEspacio=tipo_estandar,
    nombre='Tarifa Estandar 2025',
    precioHora=5000,
    precioDia=50000,
    precioMensual=500000,
    fechaInicio=date.today(),
    fechaFin=None,
    activa=True,
)
print("[OK] Tarifa Estandar 2025 (ACTIVA)")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_estandar,
    nombre='Tarifa Estandar 2024 (Antigua)',
    precioHora=4500,
    precioDia=45000,
    precioMensual=450000,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)
print("[OK] Tarifa Estandar 2024 (DESACTIVADA)")

# Tarifas Moto
Tarifa.objects.create(
    fkIdTipoEspacio=tipo_moto,
    nombre='Tarifa Motos 2025',
    precioHora=2000,
    precioDia=20000,
    precioMensual=200000,
    fechaInicio=date.today(),
    fechaFin=None,
    activa=True,
)
print("[OK] Tarifa Motos 2025 (ACTIVA)")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_moto,
    nombre='Tarifa Motos 2024 (Antigua)',
    precioHora=1800,
    precioDia=18000,
    precioMensual=180000,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)
print("[OK] Tarifa Motos 2024 (DESACTIVADA)")

# Tarifas VIP
Tarifa.objects.create(
    fkIdTipoEspacio=tipo_vip,
    nombre='Tarifa VIP 2025',
    precioHora=10000,
    precioDia=100000,
    precioMensual=1000000,
    fechaInicio=date.today(),
    fechaFin=None,
    activa=True,
)
print("[OK] Tarifa VIP 2025 (ACTIVA)")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_vip,
    nombre='Tarifa VIP 2024 (Antigua)',
    precioHora=9000,
    precioDia=90000,
    precioMensual=900000,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)
print("[OK] Tarifa VIP 2024 (DESACTIVADA)")

# 6. CREAR ESPACIOS
print("\n[6/7] Creando espacios...")
espacios_creados = 0

# Piso 1 - Espacios Estándar (15) y Motos (10)
for i in range(1, 16):
    Espacio.objects.create(
        espNumero=f'P1-A{i:02d}',
        fkIdPiso=pisos[0],
        fkIdTipoEspacio=tipo_estandar,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

for i in range(1, 11):
    Espacio.objects.create(
        espNumero=f'P1-M{i:02d}',
        fkIdPiso=pisos[0],
        fkIdTipoEspacio=tipo_moto,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

# Piso 2 - Espacios Estándar (15) y VIP (5)
for i in range(1, 16):
    Espacio.objects.create(
        espNumero=f'P2-A{i:02d}',
        fkIdPiso=pisos[1],
        fkIdTipoEspacio=tipo_estandar,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

for i in range(1, 6):
    Espacio.objects.create(
        espNumero=f'P2-V{i:02d}',
        fkIdPiso=pisos[1],
        fkIdTipoEspacio=tipo_vip,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

# Piso 3 - Espacios Estándar (20)
for i in range(1, 21):
    Espacio.objects.create(
        espNumero=f'P3-A{i:02d}',
        fkIdPiso=pisos[2],
        fkIdTipoEspacio=tipo_estandar,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

print(f"[OK] {espacios_creados} espacios creados")

# 7. CREAR VEHÍCULOS
print("\n[7/7] Creando vehículos de prueba...")
vehiculos_data = [
    ('ABC123', 'CARRO', 'Toyota', 'Corolla', cliente, False),
    ('DEF456', 'CARRO', 'Mazda', 'CX-5', cliente, False),
    ('GHI789', 'CARRO', 'Chevrolet', 'Spark', cliente, False),
    ('JKL012', 'MOTO', 'Yamaha', 'FZ-16', cliente, False),
    ('MNO345', 'MOTO', 'Suzuki', 'Gixxer', cliente, False),
    ('PQR678', 'CARRO', 'BMW', 'X5', cliente, False),
]

for placa, tipo, marca, modelo, propietario, es_visitante in vehiculos_data:
    Vehiculo.objects.create(
        vehPlaca=placa,
        vehTipo=tipo,
        vehMarca=marca,
        vehModelo=modelo,
        fkIdUsuario=propietario,
        es_visitante=es_visitante,
    )

print(f"[OK] {len(vehiculos_data)} vehículos registrados")

# 8. CREAR CUPONES DE DESCUENTO
print("\n[8/9] Creando cupones de descuento...")

from cupones.models import Cupon

cupones_data = [
    # Cupones activos
    ('Bienvenida 2025', 'PORCENTAJE', 20, 'Descuento de bienvenida para nuevos clientes', date.today(), date.today() + timedelta(days=90), True),
    ('Descuento 10%', 'PORCENTAJE', 10, 'Descuento general del 10%', date.today(), date.today() + timedelta(days=60), True),
    ('Descuento Fijo $5000', 'VALOR_FIJO', 5000, 'Descuento fijo de $5000 en tu próximo pago', date.today(), date.today() + timedelta(days=30), True),
    ('VIP Premium 2025', 'PORCENTAJE', 25, 'Descuento exclusivo para clientes VIP', date.today(), date.today() + timedelta(days=365), True),
    # Cupones desactivados
    ('Navidad 2024', 'PORCENTAJE', 30, 'Promoción especial de Navidad 2024', date(2024, 12, 1), date(2024, 12, 31), False),
    ('Verano 2024', 'PORCENTAJE', 15, 'Descuento de temporada de verano', date(2024, 6, 1), date(2024, 8, 31), False),
]

for nombre, tipo, valor, descripcion, inicio, fin, activo in cupones_data:
    Cupon.objects.create(
        cupNombre=nombre,
        cupTipo=tipo,
        cupValor=valor,
        cupDescripcion=descripcion,
        cupFechaInicio=inicio,
        cupFechaFin=fin,
        cupActivo=activo,
    )
    estado = "ACTIVO" if activo else "DESACTIVADO"
    print(f"[OK] Cupón '{nombre}' ({estado})")

# 9. MARCAR ALGUNOS ESPACIOS COMO OCUPADOS/INACTIVOS
print("\n[9/9] Configurando estados de espacios...")

# Marcar algunos espacios como OCUPADOS (simulando vehículos estacionados actualmente)
espacios_ocupar = Espacio.objects.filter(espEstado='DISPONIBLE')[:8]
vehiculos_list = list(Vehiculo.objects.all())
tarifa_std = Tarifa.objects.get(nombre='Tarifa Estandar 2025')

for idx, espacio in enumerate(espacios_ocupar):
    vehiculo = vehiculos_list[idx % len(vehiculos_list)]

    # Crear entrada sin salida (actualmente estacionado)
    hora_entrada = timezone.now() - timedelta(hours=(idx + 1))
    registro = InventarioParqueo.objects.create(
        fkIdVehiculo=vehiculo,
        fkIdEspacio=espacio,
        parHoraSalida=None,  # Sin salida = actualmente ocupado
    )
    InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada)

    # Actualizar estado del espacio
    espacio.espEstado = 'OCUPADO'
    espacio.save()

print(f"[OK] {len(espacios_ocupar)} espacios marcados como OCUPADOS")

# Marcar algunos espacios como INACTIVOS (mantenimiento)
espacios_inactivar = Espacio.objects.filter(espEstado='DISPONIBLE')[5:10]
for espacio in espacios_inactivar:
    espacio.espEstado = 'INACTIVO'
    espacio.save()

print(f"[OK] {len(espacios_inactivar)} espacios marcados como INACTIVOS (mantenimiento)")

# RESUMEN FINAL
print("\n" + "=" * 60)
print(">> BASE DE DATOS REGENERADA EXITOSAMENTE")
print("=" * 60)
print(f"Usuarios: {Usuario.objects.count()} (Admin, Cliente, Vigilante)")
print(f"Pisos: {Piso.objects.count()} (3 activos, 1 desactivado)")
print(f"Tipos de Espacio: {TipoEspacio.objects.count()}")
print(f"Espacios: {Espacio.objects.count()}")
print(f"  - Disponibles: {Espacio.objects.filter(espEstado='DISPONIBLE').count()}")
print(f"  - Ocupados: {Espacio.objects.filter(espEstado='OCUPADO').count()}")
print(f"  - Inactivos: {Espacio.objects.filter(espEstado='INACTIVO').count()}")
print(f"Tarifas: {Tarifa.objects.count()} (3 activas, 3 desactivadas)")
print(f"Vehiculos: {Vehiculo.objects.count()}")
print(f"Cupones: {Cupon.objects.count()} (4 activos, 2 desactivados)")

print("\n" + "=" * 60)
print(">> CREDENCIALES DE ACCESO")
print("=" * 60)
print("Admin:")
print("  Email: admin@multiparking.com")
print("  Password: admin123")
print("")
print("Cliente:")
print("  Email: cliente@test.com")
print("  Password: test123")
print("")
print("Vigilante:")
print("  Email: vigilante@multiparking.com")
print("  Password: vigilante123")

print("\n[INFO] Ahora ejecuta: python mantener_datos_demo.py")
print("[INFO] Para generar pagos de demostracion")
