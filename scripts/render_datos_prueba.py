# -*- coding: utf-8 -*-
"""
Script para cargar datos de prueba en Render.
Crea usuarios, pisos, espacios, tarifas, vehiculos, cupones, reservas y pagos.

Ejecutar en Render Shell:
  cd /opt/render/project/src && python scripts/render_datos_prueba.py
"""
import os
import sys
import django
from datetime import date, timedelta, datetime, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')

# Asegurar que el path del proyecto esté en sys.path
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

# ── 1. USUARIOS ─────────────────────────────────────────────
print("\n[1/11] Creando usuarios...")

admin = Usuario.objects.create(
    usuCorreo='admin@multiparking.com',
    usuDocumento='1000000001',
    usuNombreCompleto='Carlos Administrador',
    usuTelefono='3101234567',
    usuClaveHash=make_password('admin123'),
    rolTipoRol='ADMIN',
    usuEstado=True,
)
print(f"  [OK] Admin: {admin.usuCorreo}")

vigilante = Usuario.objects.create(
    usuCorreo='vigilante@multiparking.com',
    usuDocumento='1000000002',
    usuNombreCompleto='Jorge Vigilante Principal',
    usuTelefono='3109876543',
    usuClaveHash=make_password('vigilante123'),
    rolTipoRol='VIGILANTE',
    usuEstado=True,
)
print(f"  [OK] Vigilante: {vigilante.usuCorreo}")

clientes_data = [
    ('cliente@test.com', '1234567890', 'Maria Gonzalez', '3201234567', True),
    ('juan.perez@email.com', '1234567891', 'Juan Perez', '3202345678', True),
    ('ana.rodriguez@email.com', '1234567892', 'Ana Rodriguez', '3203456789', True),
    ('carlos.martinez@email.com', '1234567893', 'Carlos Martinez', '3204567890', True),
    ('laura.lopez@email.com', '1234567894', 'Laura Lopez', '3205678901', False),
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
    print(f"  [OK] Cliente: {nombre} ({estado_txt})")

# ── 2. PISOS ────────────────────────────────────────────────
print("\n[2/11] Creando pisos...")
pisos = []
for i in range(1, 5):
    piso = Piso.objects.create(
        pisNombre=f'Piso {i}',
        pisEstado=(i != 4)  # Piso 4 desactivado
    )
    pisos.append(piso)
    estado_txt = "activo" if piso.pisEstado else "DESACTIVADO"
    print(f"  [OK] {piso.pisNombre} ({estado_txt})")

# ── 3. TIPOS DE ESPACIO ────────────────────────────────────
print("\n[3/11] Creando tipos de espacio...")
tipo_estandar = TipoEspacio.objects.create(nombre='Estandar')
tipo_moto = TipoEspacio.objects.create(nombre='Moto')
tipo_vip = TipoEspacio.objects.create(nombre='VIP')
tipo_visitante = TipoEspacio.objects.create(nombre='Visitante')
print("  [OK] Tipos: Estandar, Moto, VIP, Visitante")

# ── 4. TARIFAS ──────────────────────────────────────────────
print("\n[4/11] Creando tarifas...")

tarifas_data = [
    (tipo_estandar, 'Tarifa Estandar 2025', 5000, 50000, 500000, True),
    (tipo_estandar, 'Tarifa Estandar 2024', 4500, 45000, 450000, False),
    (tipo_moto, 'Tarifa Motos 2025', 2000, 20000, 200000, True),
    (tipo_moto, 'Tarifa Motos 2024', 1800, 18000, 180000, False),
    (tipo_vip, 'Tarifa VIP 2025', 10000, 100000, 1000000, True),
    (tipo_vip, 'Tarifa VIP 2024', 9000, 90000, 900000, False),
    (tipo_visitante, 'Tarifa Visitantes 2025', 6000, 60000, 0, True),
    (tipo_visitante, 'Tarifa Visitantes 2024', 5500, 55000, 0, False),
]

for tipo_esp, nombre, hora, dia, mes, activa in tarifas_data:
    Tarifa.objects.create(
        fkIdTipoEspacio=tipo_esp,
        nombre=nombre,
        precioHora=hora,
        precioDia=dia,
        precioMensual=mes,
        fechaInicio=date.today() if activa else date(2024, 1, 1),
        fechaFin=None if activa else date(2024, 12, 31),
        activa=activa,
    )
    estado = "ACTIVA" if activa else "desactivada"
    if activa:
        print(f"  [OK] {nombre} ({estado}) - ${hora:,}/h")

# ── 5. ESPACIOS ─────────────────────────────────────────────
print("\n[5/11] Creando espacios...")
espacios_creados = 0

# Piso 1 - Estandar (12) + Motos (8) + Visitante (5)
for i in range(1, 13):
    Espacio.objects.create(espNumero=f'P1-A{i:02d}', fkIdPiso=pisos[0], fkIdTipoEspacio=tipo_estandar, espEstado='DISPONIBLE')
    espacios_creados += 1
for i in range(1, 9):
    Espacio.objects.create(espNumero=f'P1-M{i:02d}', fkIdPiso=pisos[0], fkIdTipoEspacio=tipo_moto, espEstado='DISPONIBLE')
    espacios_creados += 1
for i in range(1, 6):
    Espacio.objects.create(espNumero=f'P1-V{i:02d}', fkIdPiso=pisos[0], fkIdTipoEspacio=tipo_visitante, espEstado='DISPONIBLE')
    espacios_creados += 1

# Piso 2 - Estandar (15) + VIP (5)
for i in range(1, 16):
    Espacio.objects.create(espNumero=f'P2-A{i:02d}', fkIdPiso=pisos[1], fkIdTipoEspacio=tipo_estandar, espEstado='DISPONIBLE')
    espacios_creados += 1
for i in range(1, 6):
    Espacio.objects.create(espNumero=f'P2-VIP{i:02d}', fkIdPiso=pisos[1], fkIdTipoEspacio=tipo_vip, espEstado='DISPONIBLE')
    espacios_creados += 1

# Piso 3 - Estandar (18) + Moto (5)
for i in range(1, 19):
    Espacio.objects.create(espNumero=f'P3-A{i:02d}', fkIdPiso=pisos[2], fkIdTipoEspacio=tipo_estandar, espEstado='DISPONIBLE')
    espacios_creados += 1
for i in range(1, 6):
    Espacio.objects.create(espNumero=f'P3-M{i:02d}', fkIdPiso=pisos[2], fkIdTipoEspacio=tipo_moto, espEstado='DISPONIBLE')
    espacios_creados += 1

print(f"  [OK] {espacios_creados} espacios creados en 3 pisos")

# ── 6. VEHICULOS ────────────────────────────────────────────
print("\n[6/11] Creando vehiculos...")

vehiculos_data = [
    ('XYZ789', 'CARRO', 'Honda', 'Civic', clientes[0], False),
    ('ABC123', 'CARRO', 'Renault', 'Logan', clientes[0], False),
    ('DEF456', 'CARRO', 'Mazda', '3', clientes[1], False),
    ('GHI789', 'CARRO', 'Chevrolet', 'Onix', clientes[2], False),
    ('JKL012', 'MOTO', 'Yamaha', 'MT-03', clientes[2], False),
    ('MNO345', 'MOTO', 'Suzuki', 'GSX-R150', clientes[3], False),
    ('PQR678', 'CARRO', 'Kia', 'Sportage', clientes[3], False),
    ('STU901', 'CARRO', 'Nissan', 'Sentra', clientes[1], False),
    ('VIS001', 'CARRO', 'Toyota', 'Corolla', None, True),
    ('VIS002', 'CARRO', 'Hyundai', 'Accent', None, True),
    ('VIS003', 'MOTO', 'Honda', 'CB190R', None, True),
]

vehiculos_list = []
for placa, tipo, marca, modelo, propietario, es_visitante in vehiculos_data:
    vehiculo = Vehiculo.objects.create(
        vehPlaca=placa, vehTipo=tipo, vehMarca=marca,
        vehModelo=modelo, fkIdUsuario=propietario, es_visitante=es_visitante,
    )
    vehiculos_list.append(vehiculo)

print(f"  [OK] {len(vehiculos_data)} vehiculos (8 clientes, 3 visitantes)")

# ── 7. CUPONES ──────────────────────────────────────────────
print("\n[7/11] Creando cupones...")

cupones_data = [
    ('Mes del Cliente', 'PORCENTAJE', 15, 'Descuento especial del mes', date.today(), date.today() + timedelta(days=30), True),
    ('Primera Visita', 'VALOR_FIJO', 10000, 'Descuento para nuevos clientes', date.today(), date.today() + timedelta(days=90), True),
    ('Nocturno 20%', 'PORCENTAJE', 20, 'Descuento parqueos entre 8pm y 6am', date.today(), date.today() + timedelta(days=60), True),
    ('VIP Gold', 'PORCENTAJE', 30, 'Descuento exclusivo clientes VIP Gold', date.today(), date.today() + timedelta(days=365), True),
    ('Fin de Semana', 'VALOR_FIJO', 8000, 'Descuento sabados y domingos', date.today(), date.today() + timedelta(days=180), True),
    ('Black Friday 2024', 'PORCENTAJE', 40, 'Promocion Black Friday', date(2024, 11, 29), date(2024, 11, 30), False),
    ('Ano Nuevo 2024', 'PORCENTAJE', 25, 'Celebra el ano nuevo', date(2024, 12, 26), date(2025, 1, 2), False),
]

for nombre, tipo, valor, descripcion, inicio, fin, activo in cupones_data:
    Cupon.objects.create(
        cupNombre=nombre, cupTipo=tipo, cupValor=valor,
        cupDescripcion=descripcion, cupFechaInicio=inicio,
        cupFechaFin=fin, cupActivo=activo,
    )

print(f"  [OK] {len(cupones_data)} cupones (5 activos, 2 desactivados)")

# ── 8. ESPACIOS OCUPADOS ────────────────────────────────────
print("\n[8/11] Configurando espacios ocupados...")

espacios_ocupar = list(Espacio.objects.filter(espEstado='DISPONIBLE')[:10])

for idx, espacio in enumerate(espacios_ocupar):
    vehiculo = vehiculos_list[idx % len(vehiculos_list)]
    hora_entrada = timezone.now() - timedelta(hours=(idx + 1) * 2)

    registro = InventarioParqueo.objects.create(
        fkIdVehiculo=vehiculo, fkIdEspacio=espacio, parHoraSalida=None,
    )
    InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada)

    espacio.espEstado = 'OCUPADO'
    espacio.save()

print(f"  [OK] {len(espacios_ocupar)} espacios OCUPADOS")

# ── 9. ESPACIOS INACTIVOS ──────────────────────────────────
print("\n[9/11] Configurando espacios en mantenimiento...")

espacios_inactivar = list(Espacio.objects.filter(espEstado='DISPONIBLE')[8:15])
for espacio in espacios_inactivar:
    espacio.espEstado = 'INACTIVO'
    espacio.save()

print(f"  [OK] {len(espacios_inactivar)} espacios INACTIVOS")

# ── 10. RESERVAS ────────────────────────────────────────────
print("\n[10/11] Creando reservas...")

reservas_data = [
    (date.today(), time(14, 0), time(18, 0), 'CONFIRMADA', vehiculos_list[0]),
    (date.today(), time(10, 0), time(12, 0), 'PENDIENTE', vehiculos_list[1]),
    (date.today() + timedelta(days=1), time(8, 0), time(17, 0), 'CONFIRMADA', vehiculos_list[2]),
    (date.today() + timedelta(days=1), time(9, 0), time(13, 0), 'CONFIRMADA', vehiculos_list[3]),
    (date.today() + timedelta(days=1), time(15, 0), time(19, 0), 'PENDIENTE', vehiculos_list[4]),
    (date.today() + timedelta(days=2), time(7, 0), time(16, 0), 'CONFIRMADA', vehiculos_list[5]),
    (date.today() + timedelta(days=2), time(11, 0), time(14, 0), 'PENDIENTE', vehiculos_list[6]),
    (date.today() + timedelta(days=5), time(8, 0), time(18, 0), 'CONFIRMADA', vehiculos_list[0]),
    (date.today() + timedelta(days=7), time(9, 0), time(17, 0), 'PENDIENTE', vehiculos_list[1]),
    (date.today() + timedelta(days=3), time(10, 0), time(15, 0), 'CANCELADA', vehiculos_list[2]),
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

# ── 11. PAGOS (ultimos 7 dias para la grafica) ─────────────
print("\n[11/11] Generando pagos de los ultimos 7 dias...")

now = timezone.now()
hoy_local = timezone.localtime(now).date()
tarifa = Tarifa.objects.filter(activa=True).first()
pagos_creados = 0

if tarifa:
    for dia_offset in range(5):
        dia_fecha = hoy_local - timedelta(days=dia_offset)

        for i in range(3):
            vehiculo = vehiculos_list[i % len(vehiculos_list)]
            espacio = Espacio.objects.filter(espEstado='DISPONIBLE').first()

            if not espacio:
                espacio = Espacio.objects.first()

            if not espacio:
                break

            hora_base = 10 + (i * 2)  # 10am, 12pm, 2pm

            hora_entrada_naive = datetime(dia_fecha.year, dia_fecha.month, dia_fecha.day, hora_base, 0, 0)
            hora_salida_naive = datetime(dia_fecha.year, dia_fecha.month, dia_fecha.day, hora_base + 3, 0, 0)

            hora_entrada_dt = timezone.make_aware(hora_entrada_naive)
            hora_salida_dt = timezone.make_aware(hora_salida_naive)

            # Crear registro de inventario (bypass auto_now_add con update)
            registro = InventarioParqueo.objects.create(
                fkIdVehiculo=vehiculo, fkIdEspacio=espacio,
                parHoraSalida=hora_salida_dt,
            )
            InventarioParqueo.objects.filter(pk=registro.pk).update(parHoraEntrada=hora_entrada_dt)

            # Calcular monto (3 horas * tarifa)
            monto = float(tarifa.precioHora) * 3

            # Crear pago (bypass auto_now_add con update)
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
print(f"  Usuarios:   {Usuario.objects.count()} (1 admin, 1 vigilante, {Usuario.objects.filter(rolTipoRol='CLIENTE').count()} clientes)")
print(f"  Pisos:      {Piso.objects.count()} (3 activos, 1 desactivado)")
print(f"  Tipos Esp:  {TipoEspacio.objects.count()} (Estandar, Moto, VIP, Visitante)")
print(f"  Espacios:   {Espacio.objects.count()}")
print(f"    - Disponibles: {Espacio.objects.filter(espEstado='DISPONIBLE').count()}")
print(f"    - Ocupados:    {Espacio.objects.filter(espEstado='OCUPADO').count()}")
print(f"    - Inactivos:   {Espacio.objects.filter(espEstado='INACTIVO').count()}")
print(f"  Tarifas:    {Tarifa.objects.count()} (4 activas, 4 desactivadas)")
print(f"  Vehiculos:  {Vehiculo.objects.count()} (8 clientes, 3 visitantes)")
print(f"  Cupones:    {Cupon.objects.count()} (5 activos, 2 desactivados)")
print(f"  Reservas:   {Reserva.objects.count()}")
print(f"  Pagos:      {Pago.objects.count()}")

print("\n" + "=" * 60)
print("  CREDENCIALES DE ACCESO")
print("=" * 60)
print("  Admin:      admin@multiparking.com / admin123")
print("  Vigilante:  vigilante@multiparking.com / vigilante123")
print("  Cliente:    cliente@test.com / test123")
print("=" * 60)
