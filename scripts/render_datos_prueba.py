# -*- coding: utf-8 -*-
"""
Script para cargar datos de prueba en Render.
Limpia la BD y crea usuarios, pisos, espacios, tarifas, vehiculos,
cupones, reservas y pagos de demo.

Ejecutar en Render Shell:
  cd /opt/render/project/src && python scripts/render_datos_prueba.py
"""
import os
import sys
import django
from datetime import date, timedelta, datetime, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

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
print("  CARGANDO DATOS DE PRUEBA - MultiParking (Render)")
print("=" * 60)

# ── 1. LIMPIAR TODO ─────────────────────────────────────────
print("\n[1/11] Limpiando base de datos...")
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
print("  [OK] Base de datos limpiada completamente")

# ── 2. USUARIOS ─────────────────────────────────────────────
print("\n[2/11] Creando usuarios...")

admin = Usuario.objects.create(
    usuCorreo='admin@multiparking.com',
    usuDocumento='0000000001',
    usuNombreCompleto='Administrador Principal',
    usuTelefono='3000000000',
    usuClaveHash=make_password('admin123'),
    rolTipoRol='ADMIN',
    usuEstado=True,
)
print(f"  [OK] Admin: admin@multiparking.com / admin123")

vigilante = Usuario.objects.create(
    usuCorreo='vigilante@multiparking.com',
    usuDocumento='0000000002',
    usuNombreCompleto='Vigilante Principal',
    usuTelefono='3001111111',
    usuClaveHash=make_password('vigil123'),
    rolTipoRol='VIGILANTE',
    usuEstado=True,
)
print(f"  [OK] Vigilante: vigilante@multiparking.com / vigil123")

cliente1 = Usuario.objects.create(
    usuCorreo='cliente@test.com',
    usuDocumento='1234567890',
    usuNombreCompleto='Carlos Perez',
    usuTelefono='3001234567',
    usuClaveHash=make_password('test123'),
    rolTipoRol='CLIENTE',
    usuEstado=True,
)
print(f"  [OK] Cliente 1: cliente@test.com / test123")

cliente2 = Usuario.objects.create(
    usuCorreo='maria@test.com',
    usuDocumento='9876543210',
    usuNombreCompleto='Maria Lopez',
    usuTelefono='3009876543',
    usuClaveHash=make_password('test123'),
    rolTipoRol='CLIENTE',
    usuEstado=True,
)
print(f"  [OK] Cliente 2: maria@test.com / test123")

# ── 3. TIPOS DE ESPACIO (Solo Carro y Moto) ─────────────────
print("\n[3/11] Creando tipos de espacio...")
tipo_carro = TipoEspacio.objects.create(nombre='Carro')
tipo_moto = TipoEspacio.objects.create(nombre='Moto')
print("  [OK] Tipos: Carro, Moto")

# ── 4. PISOS ────────────────────────────────────────────────
print("\n[4/11] Creando pisos...")

pisos_config = [
    ('Piso 1 - Subsuelo', True),
    ('Piso 2 - Nivel Calle', True),
    ('Piso 3 - Terraza', True),
    ('Piso 4 - Mantenimiento', False),
]

pisos = []
for nombre, estado in pisos_config:
    piso = Piso.objects.create(pisNombre=nombre, pisEstado=estado)
    pisos.append(piso)
    estado_txt = "activo" if estado else "DESACTIVADO"
    print(f"  [OK] {nombre} ({estado_txt})")

# ── 5. ESPACIOS ─────────────────────────────────────────────
print("\n[5/11] Creando espacios...")

espacios_config = [
    (0, 'C1', tipo_carro, 15),   # Piso 1: 15 carros
    (0, 'M1', tipo_moto, 10),    # Piso 1: 10 motos
    (1, 'C2', tipo_carro, 20),   # Piso 2: 20 carros
    (1, 'M2', tipo_moto, 8),     # Piso 2: 8 motos
    (2, 'C3', tipo_carro, 12),   # Piso 3: 12 carros
    (2, 'M3', tipo_moto, 6),     # Piso 3: 6 motos
]

total_espacios = 0
for piso_idx, prefijo, tipo, cantidad in espacios_config:
    for i in range(1, cantidad + 1):
        Espacio.objects.create(
            espNumero=f'{prefijo}-{i:02d}',
            fkIdPiso=pisos[piso_idx],
            fkIdTipoEspacio=tipo,
            espEstado='DISPONIBLE',
        )
        total_espacios += 1

carros = Espacio.objects.filter(fkIdTipoEspacio=tipo_carro).count()
motos = Espacio.objects.filter(fkIdTipoEspacio=tipo_moto).count()
print(f"  [OK] {total_espacios} espacios creados (Carros: {carros}, Motos: {motos})")

# ── 6. TARIFAS ──────────────────────────────────────────────
print("\n[6/11] Creando tarifas...")

Tarifa.objects.create(
    nombre='Tarifa Carros 2026',
    fkIdTipoEspacio=tipo_carro,
    precioHora=5000,
    precioHoraVisitante=7000,
    precioDia=40000,
    precioMensual=450000,
    fechaInicio=date.today(),
    activa=True,
)
print("  [OK] Tarifa Carros 2026: $5,000/h | Visitante $7,000/h (ACTIVA)")

Tarifa.objects.create(
    nombre='Tarifa Carros 2025 (Antigua)',
    fkIdTipoEspacio=tipo_carro,
    precioHora=4500,
    precioHoraVisitante=6000,
    precioDia=35000,
    precioMensual=400000,
    fechaInicio=date(2025, 1, 1),
    fechaFin=date(2025, 12, 31),
    activa=False,
)
print("  [OK] Tarifa Carros 2025 (DESACTIVADA)")

Tarifa.objects.create(
    nombre='Tarifa Motos 2026',
    fkIdTipoEspacio=tipo_moto,
    precioHora=2000,
    precioHoraVisitante=3000,
    precioDia=18000,
    precioMensual=180000,
    fechaInicio=date.today(),
    activa=True,
)
print("  [OK] Tarifa Motos 2026: $2,000/h | Visitante $3,000/h (ACTIVA)")

Tarifa.objects.create(
    nombre='Tarifa Motos 2025 (Antigua)',
    fkIdTipoEspacio=tipo_moto,
    precioHora=1800,
    precioHoraVisitante=2500,
    precioDia=15000,
    precioMensual=150000,
    fechaInicio=date(2025, 1, 1),
    fechaFin=date(2025, 12, 31),
    activa=False,
)
print("  [OK] Tarifa Motos 2025 (DESACTIVADA)")

# ── 7. VEHICULOS ────────────────────────────────────────────
print("\n[7/11] Creando vehiculos...")

vehiculos_demo = [
    ('ABC123', 'CARRO', 'Rojo', 'Toyota', 'Corolla', cliente1),
    ('DEF456', 'CARRO', 'Blanco', 'Mazda', '3', cliente1),
    ('GHI789', 'MOTO', 'Negro', 'Yamaha', 'FZ250', cliente1),
    ('JKL012', 'CARRO', 'Gris', 'Chevrolet', 'Spark', cliente2),
    ('MNO345', 'MOTO', 'Azul', 'Suzuki', 'GN125', cliente2),
    ('PQR678', 'CARRO', 'Negro', 'Renault', 'Logan', cliente2),
]

vehiculos = []
for placa, tipo, color, marca, modelo, propietario in vehiculos_demo:
    v = Vehiculo.objects.create(
        vehPlaca=placa, vehTipo=tipo, vehColor=color,
        vehMarca=marca, vehModelo=modelo,
        fkIdUsuario=propietario, es_visitante=False,
    )
    vehiculos.append(v)

# Vehiculos visitante
vehiculos_visitante = []
for placa, tipo, color, marca, modelo in [
    ('VIS001', 'CARRO', 'Plata', 'Hyundai', 'Accent'),
    ('VIS002', 'MOTO', 'Rojo', 'Honda', 'CB190R'),
]:
    v = Vehiculo.objects.create(
        vehPlaca=placa, vehTipo=tipo, vehColor=color,
        vehMarca=marca, vehModelo=modelo,
        fkIdUsuario=None, es_visitante=True,
    )
    vehiculos_visitante.append(v)

print(f"  [OK] {len(vehiculos)} vehiculos de clientes + {len(vehiculos_visitante)} visitantes")

# ── 8. CUPONES ──────────────────────────────────────────────
print("\n[8/11] Creando cupones...")

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
        'cupActivo': True,
    },
    {
        'cupNombre': 'Descuento Fijo $5,000',
        'cupCodigo': 'DESCUENTO5K',
        'cupTipo': 'VALOR_FIJO',
        'cupValor': 5000,
        'cupDescripcion': '$5,000 de descuento directo en tu pago',
        'cupFechaInicio': hoy,
        'cupFechaFin': hoy + timedelta(days=60),
        'cupActivo': True,
    },
    {
        'cupNombre': 'Promo Fin de Semana',
        'cupCodigo': 'FINDE50',
        'cupTipo': 'PORCENTAJE',
        'cupValor': 50,
        'cupDescripcion': '50% de descuento los fines de semana',
        'cupFechaInicio': hoy,
        'cupFechaFin': hoy + timedelta(days=30),
        'cupActivo': True,
    },
    {
        'cupNombre': 'VIP Premium',
        'cupCodigo': 'VIPPREMIUM',
        'cupTipo': 'PORCENTAJE',
        'cupValor': 30,
        'cupDescripcion': 'Descuento exclusivo para clientes VIP',
        'cupFechaInicio': hoy,
        'cupFechaFin': hoy + timedelta(days=365),
        'cupActivo': True,
    },
    {
        'cupNombre': 'Navidad 2025',
        'cupCodigo': 'NAVIDAD2025',
        'cupTipo': 'PORCENTAJE',
        'cupValor': 30,
        'cupDescripcion': 'Promocion especial de Navidad 2025',
        'cupFechaInicio': date(2025, 12, 1),
        'cupFechaFin': date(2025, 12, 31),
        'cupActivo': False,
    },
    {
        'cupNombre': 'Black Friday 2025',
        'cupCodigo': 'BLACKFRIDAY',
        'cupTipo': 'PORCENTAJE',
        'cupValor': 40,
        'cupDescripcion': 'Descuento Black Friday',
        'cupFechaInicio': date(2025, 11, 25),
        'cupFechaFin': date(2025, 11, 30),
        'cupActivo': False,
    },
]

for cupon_data in cupones_demo:
    Cupon.objects.create(**cupon_data)
    estado = "ACTIVO" if cupon_data['cupActivo'] else "DESACTIVADO"
    print(f"  [OK] {cupon_data['cupNombre']} -> {cupon_data['cupCodigo']} ({estado})")

# ── 9. ESPACIOS OCUPADOS ────────────────────────────────────
print("\n[9/11] Simulando vehiculos estacionados...")

espacios_disponibles = list(Espacio.objects.filter(espEstado='DISPONIBLE')[:6])
vehiculos_a_parquear = vehiculos[:6]

parqueados = 0
for idx in range(min(len(espacios_disponibles), len(vehiculos_a_parquear))):
    espacio = espacios_disponibles[idx]
    vehiculo = vehiculos_a_parquear[idx]

    hora_entrada = timezone.now() - timedelta(hours=(idx + 1))
    registro = InventarioParqueo.objects.create(
        fkIdVehiculo=vehiculo,
        fkIdEspacio=espacio,
        parHoraSalida=None,
    )
    InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada)

    espacio.espEstado = 'OCUPADO'
    espacio.save()
    parqueados += 1

print(f"  [OK] {parqueados} vehiculos estacionados actualmente")

# Marcar algunos espacios como INACTIVOS (mantenimiento)
espacios_inactivar = list(Espacio.objects.filter(espEstado='DISPONIBLE')[10:15])
for espacio in espacios_inactivar:
    espacio.espEstado = 'INACTIVO'
    espacio.save()

print(f"  [OK] {len(espacios_inactivar)} espacios en mantenimiento (INACTIVO)")

# ── 10. RESERVAS ────────────────────────────────────────────
print("\n[10/11] Creando reservas...")

reservas_data = [
    (hoy, time(14, 0), time(18, 0), 'CONFIRMADA', vehiculos[0]),
    (hoy, time(10, 0), time(12, 0), 'PENDIENTE', vehiculos[1]),
    (hoy + timedelta(days=1), time(8, 0), time(17, 0), 'CONFIRMADA', vehiculos[2]),
    (hoy + timedelta(days=1), time(9, 0), time(13, 0), 'CONFIRMADA', vehiculos[3]),
    (hoy + timedelta(days=1), time(15, 0), time(19, 0), 'PENDIENTE', vehiculos[4]),
    (hoy + timedelta(days=2), time(7, 0), time(16, 0), 'CONFIRMADA', vehiculos[5]),
    (hoy + timedelta(days=2), time(11, 0), time(14, 0), 'PENDIENTE', vehiculos[0]),
    (hoy + timedelta(days=5), time(8, 0), time(18, 0), 'CONFIRMADA', vehiculos[1]),
    (hoy + timedelta(days=7), time(9, 0), time(17, 0), 'PENDIENTE', vehiculos[2]),
    (hoy + timedelta(days=3), time(10, 0), time(15, 0), 'CANCELADA', vehiculos[3]),
]

espacios_disponibles_reserva = list(Espacio.objects.filter(espEstado='DISPONIBLE'))

for idx, (fecha, hora_inicio, hora_fin, estado, vehiculo) in enumerate(reservas_data):
    espacio = espacios_disponibles_reserva[idx % len(espacios_disponibles_reserva)]
    Reserva.objects.create(
        resFechaReserva=fecha, resHoraInicio=hora_inicio,
        resHoraFin=hora_fin, resEstado=estado,
        fkIdEspacio=espacio, fkIdVehiculo=vehiculo,
    )

print(f"  [OK] {len(reservas_data)} reservas creadas")

# ── 11. PAGOS (ultimos 5 dias para la grafica) ──────────────
print("\n[11/11] Generando pagos de los ultimos 5 dias...")

now = timezone.now()
hoy_local = timezone.localtime(now).date()
tarifa = Tarifa.objects.filter(activa=True).first()
pagos_creados = 0

if tarifa:
    for dia_offset in range(5):
        dia_fecha = hoy_local - timedelta(days=dia_offset)

        for i in range(3):
            vehiculo = vehiculos[i % len(vehiculos)]
            espacio = Espacio.objects.filter(espEstado='DISPONIBLE').first()

            if not espacio:
                espacio = Espacio.objects.first()

            if not espacio:
                break

            hora_base = 10 + (i * 2)

            hora_entrada_naive = datetime(dia_fecha.year, dia_fecha.month, dia_fecha.day, hora_base, 0, 0)
            hora_salida_naive = datetime(dia_fecha.year, dia_fecha.month, dia_fecha.day, hora_base + 3, 0, 0)

            hora_entrada_dt = timezone.make_aware(hora_entrada_naive)
            hora_salida_dt = timezone.make_aware(hora_salida_naive)

            registro = InventarioParqueo.objects.create(
                fkIdVehiculo=vehiculo, fkIdEspacio=espacio,
                parHoraSalida=hora_salida_dt,
            )
            InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada_dt)

            monto = float(tarifa.precioHora) * 3

            pago = Pago.objects.create(
                pagMonto=monto, pagMetodo='EFECTIVO',
                pagEstado='PAGADO', fkIdParqueo=registro,
            )
            Pago.objects.filter(pk=pago.pk).update(pagFechaPago=hora_salida_dt)
            pagos_creados += 1

print(f"  [OK] {pagos_creados} pagos generados (5 dias x 3 pagos)")

# ── RESUMEN FINAL ───────────────────────────────────────────
print("\n" + "=" * 60)
print("  DATOS DE PRUEBA CARGADOS EXITOSAMENTE")
print("=" * 60)
print(f"""
  Usuarios:    {Usuario.objects.count()}
  Pisos:       {Piso.objects.filter(pisEstado=True).count()} activos + {Piso.objects.filter(pisEstado=False).count()} desactivado
  Tipos:       Carro, Moto
  Espacios:    {Espacio.objects.count()} total
    Disponible:  {Espacio.objects.filter(espEstado='DISPONIBLE').count()}
    Ocupado:     {Espacio.objects.filter(espEstado='OCUPADO').count()}
    Inactivo:    {Espacio.objects.filter(espEstado='INACTIVO').count()}
  Tarifas:     {Tarifa.objects.filter(activa=True).count()} activas + {Tarifa.objects.filter(activa=False).count()} desactivadas
  Vehiculos:   {Vehiculo.objects.count()} ({len(vehiculos)} clientes, {len(vehiculos_visitante)} visitantes)
  Cupones:     {Cupon.objects.filter(cupActivo=True).count()} activos + {Cupon.objects.filter(cupActivo=False).count()} desactivados
  Reservas:    {Reserva.objects.count()}
  Pagos:       {Pago.objects.count()}
""")

print("=" * 60)
print("  CREDENCIALES DE ACCESO")
print("=" * 60)
print("""
  Admin:
    Email:    admin@multiparking.com
    Password: admin123

  Vigilante:
    Email:    vigilante@multiparking.com
    Password: vigil123

  Cliente 1 (Carlos Perez):
    Email:    cliente@test.com
    Password: test123

  Cliente 2 (Maria Lopez):
    Email:    maria@test.com
    Password: test123
""")

print("=" * 60)
print("  CUPONES DE DESCUENTO")
print("=" * 60)
print("""
  BIENVENIDO20  -> 20% descuento
  DESCUENTO5K   -> $5,000 de descuento fijo
  FINDE50       -> 50% descuento
  VIPPREMIUM    -> 30% descuento
""")
print("=" * 60)
