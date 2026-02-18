# -*- coding: utf-8 -*-
"""
Script para limpiar y regenerar la base de datos con datos variados
Incluye reservas, tarifa de visitantes y datos más realistas
Ejecutar: python reiniciar_base_datos_v2.py
"""
import os
import django
import sys
from datetime import date, timedelta, datetime, time

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
print(">> REGENERANDO BASE DE DATOS")
print(">> Version 2 - Con reservas y tarifa visitantes")
print("=" * 60)

# 1. LIMPIAR TODO
print("\n[1/10] Limpiando base de datos...")
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
print("\n[2/10] Creando usuarios...")

# Admin
admin = Usuario.objects.create(
    usuCorreo='admin@multiparking.com',
    usuDocumento='1000000001',
    usuNombreCompleto='Carlos Administrador',
    usuTelefono='3101234567',
    usuClaveHash=make_password('admin123'),
    rolTipoRol='ADMIN',
    usuEstado=True,
)
print(f"[OK] Admin: {admin.usuCorreo}")

# Vigilante
vigilante = Usuario.objects.create(
    usuCorreo='vigilante@multiparking.com',
    usuDocumento='1000000002',
    usuNombreCompleto='Jorge Vigilante Principal',
    usuTelefono='3109876543',
    usuClaveHash=make_password('vigilante123'),
    rolTipoRol='VIGILANTE',
    usuEstado=True,
)
print(f"[OK] Vigilante: {vigilante.usuCorreo}")

# Clientes
clientes_data = [
    ('cliente@test.com', '1234567890', 'María González', '3201234567', True),
    ('juan.perez@email.com', '1234567891', 'Juan Pérez', '3202345678', True),
    ('ana.rodriguez@email.com', '1234567892', 'Ana Rodríguez', '3203456789', True),
    ('carlos.martinez@email.com', '1234567893', 'Carlos Martínez', '3204567890', True),
    ('laura.lopez@email.com', '1234567894', 'Laura López', '3205678901', False),  # Desactivado
]

clientes = []
for correo, doc, nombre, tel, estado in clientes_data:
    cliente = Usuario.objects.create(
        usuCorreo=correo,
        usuDocumento=doc,
        usuNombreCompleto=nombre,
        usuTelefono=tel,
        usuClaveHash=make_password('test123'),
        rolTipoRol='CLIENTE',
        usuEstado=estado,
    )
    clientes.append(cliente)
    estado_txt = "activo" if estado else "DESACTIVADO"
    print(f"[OK] Cliente: {nombre} ({estado_txt})")

# 3. CREAR PISOS (4 pisos, 1 desactivado)
print("\n[3/10] Creando pisos...")
pisos = []
for i in range(1, 5):
    piso = Piso.objects.create(
        pisNombre=f'Piso {i}',
        pisEstado=(i != 4)  # Piso 4 desactivado
    )
    pisos.append(piso)
    estado_txt = "activo" if piso.pisEstado else "DESACTIVADO"
    print(f"[OK] {piso.pisNombre} ({estado_txt})")

# 4. CREAR TIPOS DE ESPACIO (incluye Visitante)
print("\n[4/10] Creando tipos de espacio...")
tipo_estandar = TipoEspacio.objects.create(nombre='Estandar')
tipo_moto = TipoEspacio.objects.create(nombre='Moto')
tipo_vip = TipoEspacio.objects.create(nombre='VIP')
tipo_visitante = TipoEspacio.objects.create(nombre='Visitante')
print(f"[OK] Tipos: Estandar, Moto, VIP, Visitante")

# 5. CREAR TARIFAS (2 por tipo, 1 activa y 1 desactivada)
print("\n[5/10] Creando tarifas...")

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
print("[OK] Tarifa Estandar 2025 (ACTIVA) - $5,000/h")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_estandar,
    nombre='Tarifa Estandar 2024',
    precioHora=4500,
    precioDia=45000,
    precioMensual=450000,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)

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
print("[OK] Tarifa Motos 2025 (ACTIVA) - $2,000/h")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_moto,
    nombre='Tarifa Motos 2024',
    precioHora=1800,
    precioDia=18000,
    precioMensual=180000,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)

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
print("[OK] Tarifa VIP 2025 (ACTIVA) - $10,000/h")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_vip,
    nombre='Tarifa VIP 2024',
    precioHora=9000,
    precioDia=90000,
    precioMensual=900000,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)

# Tarifas Visitante (solo activa)
Tarifa.objects.create(
    fkIdTipoEspacio=tipo_visitante,
    nombre='Tarifa Visitantes 2025',
    precioHora=6000,
    precioDia=60000,
    precioMensual=0,  # Visitantes no tienen tarifa mensual
    fechaInicio=date.today(),
    fechaFin=None,
    activa=True,
)
print("[OK] Tarifa Visitantes 2025 (ACTIVA) - $6,000/h")

Tarifa.objects.create(
    fkIdTipoEspacio=tipo_visitante,
    nombre='Tarifa Visitantes 2024',
    precioHora=5500,
    precioDia=55000,
    precioMensual=0,
    fechaInicio=date(2024, 1, 1),
    fechaFin=date(2024, 12, 31),
    activa=False,
)

# 6. CREAR ESPACIOS
print("\n[6/10] Creando espacios...")
espacios_creados = 0

# Piso 1 - Estándar (12) + Motos (8) + Visitante (5)
for i in range(1, 13):
    Espacio.objects.create(
        espNumero=f'P1-A{i:02d}',
        fkIdPiso=pisos[0],
        fkIdTipoEspacio=tipo_estandar,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

for i in range(1, 9):
    Espacio.objects.create(
        espNumero=f'P1-M{i:02d}',
        fkIdPiso=pisos[0],
        fkIdTipoEspacio=tipo_moto,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

for i in range(1, 6):
    Espacio.objects.create(
        espNumero=f'P1-V{i:02d}',
        fkIdPiso=pisos[0],
        fkIdTipoEspacio=tipo_visitante,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

# Piso 2 - Estándar (15) + VIP (5)
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
        espNumero=f'P2-VIP{i:02d}',
        fkIdPiso=pisos[1],
        fkIdTipoEspacio=tipo_vip,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

# Piso 3 - Estándar (18) + Moto (5)
for i in range(1, 19):
    Espacio.objects.create(
        espNumero=f'P3-A{i:02d}',
        fkIdPiso=pisos[2],
        fkIdTipoEspacio=tipo_estandar,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

for i in range(1, 6):
    Espacio.objects.create(
        espNumero=f'P3-M{i:02d}',
        fkIdPiso=pisos[2],
        fkIdTipoEspacio=tipo_moto,
        espEstado='DISPONIBLE',
    )
    espacios_creados += 1

print(f"[OK] {espacios_creados} espacios creados")

# 7. CREAR VEHÍCULOS (más variedad)
print("\n[7/10] Creando vehículos...")
vehiculos_data = [
    # Vehículos de clientes registrados
    ('XYZ789', 'CARRO', 'Honda', 'Civic', clientes[0], False),
    ('ABC123', 'CARRO', 'Renault', 'Logan', clientes[0], False),
    ('DEF456', 'CARRO', 'Mazda', '3', clientes[1], False),
    ('GHI789', 'CARRO', 'Chevrolet', 'Onix', clientes[2], False),
    ('JKL012', 'MOTO', 'Yamaha', 'MT-03', clientes[2], False),
    ('MNO345', 'MOTO', 'Suzuki', 'GSX-R150', clientes[3], False),
    ('PQR678', 'CARRO', 'Kia', 'Sportage', clientes[3], False),
    ('STU901', 'CARRO', 'Nissan', 'Sentra', clientes[1], False),
    # Vehículos de visitantes
    ('VIS001', 'CARRO', 'Toyota', 'Corolla', None, True),
    ('VIS002', 'CARRO', 'Hyundai', 'Accent', None, True),
    ('VIS003', 'MOTO', 'Honda', 'CB190R', None, True),
]

vehiculos_list = []
for placa, tipo, marca, modelo, propietario, es_visitante in vehiculos_data:
    vehiculo = Vehiculo.objects.create(
        vehPlaca=placa,
        vehTipo=tipo,
        vehMarca=marca,
        vehModelo=modelo,
        fkIdUsuario=propietario,
        es_visitante=es_visitante,
    )
    vehiculos_list.append(vehiculo)

print(f"[OK] {len(vehiculos_data)} vehículos registrados (8 clientes, 3 visitantes)")

# 8. CREAR CUPONES DE DESCUENTO
print("\n[8/10] Creando cupones de descuento...")

cupones_data = [
    # Cupones activos
    ('Mes del Cliente', 'PORCENTAJE', 15, 'Descuento especial del mes', date.today(), date.today() + timedelta(days=30), True),
    ('Primera Visita', 'VALOR_FIJO', 10000, 'Descuento para nuevos clientes en su primera visita', date.today(), date.today() + timedelta(days=90), True),
    ('Nocturno 20%', 'PORCENTAJE', 20, 'Descuento para parqueos entre 8pm y 6am', date.today(), date.today() + timedelta(days=60), True),
    ('VIP Gold', 'PORCENTAJE', 30, 'Descuento exclusivo para clientes VIP Gold', date.today(), date.today() + timedelta(days=365), True),
    ('Fin de Semana', 'VALOR_FIJO', 8000, 'Descuento para sabados y domingos', date.today(), date.today() + timedelta(days=180), True),
    # Cupones desactivados/expirados
    ('Black Friday 2024', 'PORCENTAJE', 40, 'Promoción especial Black Friday', date(2024, 11, 29), date(2024, 11, 30), False),
    ('Año Nuevo 2024', 'PORCENTAJE', 25, 'Celebra el año nuevo con descuento', date(2024, 12, 26), date(2025, 1, 2), False),
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
print("\n[9/10] Configurando estados de espacios...")

# Marcar algunos espacios como OCUPADOS
espacios_ocupar = Espacio.objects.filter(espEstado='DISPONIBLE')[:10]

for idx, espacio in enumerate(espacios_ocupar):
    vehiculo = vehiculos_list[idx % len(vehiculos_list)]
    hora_entrada = timezone.now() - timedelta(hours=(idx + 1) * 2)

    registro = InventarioParqueo.objects.create(
        fkIdVehiculo=vehiculo,
        fkIdEspacio=espacio,
        parHoraSalida=None,
    )
    InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada)

    espacio.espEstado = 'OCUPADO'
    espacio.save()

print(f"[OK] {len(espacios_ocupar)} espacios marcados como OCUPADOS")

# Marcar algunos espacios como INACTIVOS (mantenimiento)
espacios_inactivar = Espacio.objects.filter(espEstado='DISPONIBLE')[8:15]
for espacio in espacios_inactivar:
    espacio.espEstado = 'INACTIVO'
    espacio.save()

print(f"[OK] {len(espacios_inactivar)} espacios marcados como INACTIVOS")

# 10. CREAR RESERVAS
print("\n[10/10] Creando reservas...")

# Reservas para hoy y próximos días
reservas_data = [
    # Reservas para hoy
    (date.today(), time(14, 0), time(18, 0), 'CONFIRMADA', vehiculos_list[0]),
    (date.today(), time(10, 0), time(12, 0), 'PENDIENTE', vehiculos_list[1]),

    # Reservas para mañana
    (date.today() + timedelta(days=1), time(8, 0), time(17, 0), 'CONFIRMADA', vehiculos_list[2]),
    (date.today() + timedelta(days=1), time(9, 0), time(13, 0), 'CONFIRMADA', vehiculos_list[3]),
    (date.today() + timedelta(days=1), time(15, 0), time(19, 0), 'PENDIENTE', vehiculos_list[4]),

    # Reservas para pasado mañana
    (date.today() + timedelta(days=2), time(7, 0), time(16, 0), 'CONFIRMADA', vehiculos_list[5]),
    (date.today() + timedelta(days=2), time(11, 0), time(14, 0), 'PENDIENTE', vehiculos_list[6]),

    # Reservas futuras
    (date.today() + timedelta(days=5), time(8, 0), time(18, 0), 'CONFIRMADA', vehiculos_list[0]),
    (date.today() + timedelta(days=7), time(9, 0), time(17, 0), 'PENDIENTE', vehiculos_list[1]),

    # Reserva cancelada
    (date.today() + timedelta(days=3), time(10, 0), time(15, 0), 'CANCELADA', vehiculos_list[2]),
]

espacios_disponibles_reserva = list(Espacio.objects.filter(espEstado='DISPONIBLE'))

for idx, (fecha, hora_inicio, hora_fin, estado, vehiculo) in enumerate(reservas_data):
    espacio = espacios_disponibles_reserva[idx % len(espacios_disponibles_reserva)]

    Reserva.objects.create(
        resFechaReserva=fecha,
        resHoraInicio=hora_inicio,
        resHoraFin=hora_fin,
        resEstado=estado,
        fkIdEspacio=espacio,
        fkIdVehiculo=vehiculo,
    )

print(f"[OK] {len(reservas_data)} reservas creadas")
print(f"    - Confirmadas: {sum(1 for r in reservas_data if r[3] == 'CONFIRMADA')}")
print(f"    - Pendientes: {sum(1 for r in reservas_data if r[3] == 'PENDIENTE')}")
print(f"    - Canceladas: {sum(1 for r in reservas_data if r[3] == 'CANCELADA')}")

# RESUMEN FINAL
print("\n" + "=" * 60)
print(">> BASE DE DATOS REGENERADA EXITOSAMENTE")
print("=" * 60)
print(f"Usuarios: {Usuario.objects.count()}")
print(f"  - Admin: 1, Vigilante: 1, Clientes: {Usuario.objects.filter(rolTipoRol='CLIENTE').count()}")
print(f"Pisos: {Piso.objects.count()} (3 activos, 1 desactivado)")
print(f"Tipos de Espacio: {TipoEspacio.objects.count()} (incluye Visitante)")
print(f"Espacios: {Espacio.objects.count()}")
print(f"  - Disponibles: {Espacio.objects.filter(espEstado='DISPONIBLE').count()}")
print(f"  - Ocupados: {Espacio.objects.filter(espEstado='OCUPADO').count()}")
print(f"  - Inactivos: {Espacio.objects.filter(espEstado='INACTIVO').count()}")
print(f"Tarifas: {Tarifa.objects.count()} (4 activas, 4 desactivadas)")
print(f"Vehiculos: {Vehiculo.objects.count()} (8 clientes, 3 visitantes)")
print(f"Cupones: {Cupon.objects.count()} (5 activos, 2 desactivados)")
print(f"Reservas: {Reserva.objects.count()}")
print(f"  - Confirmadas: {Reserva.objects.filter(resEstado='CONFIRMADA').count()}")
print(f"  - Pendientes: {Reserva.objects.filter(resEstado='PENDIENTE').count()}")
print(f"  - Canceladas: {Reserva.objects.filter(resEstado='CANCELADA').count()}")

print("\n" + "=" * 60)
print(">> CREDENCIALES DE ACCESO")
print("=" * 60)
print("Admin:")
print("  Email: admin@multiparking.com")
print("  Password: admin123")
print("")
print("Vigilante:")
print("  Email: vigilante@multiparking.com")
print("  Password: vigilante123")
print("")
print("Cliente principal:")
print("  Email: cliente@test.com")
print("  Password: test123")

print("\n[INFO] Ahora ejecuta: python mantener_datos_demo.py")
print("[INFO] Para generar pagos de demostracion")
