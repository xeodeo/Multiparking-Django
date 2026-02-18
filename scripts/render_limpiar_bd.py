# -*- coding: utf-8 -*-
"""
Script para limpiar la base de datos en Render.
Elimina todos los datos respetando el orden de foreign keys.

Ejecutar en Render Shell:
  cd /opt/render/project/src && python scripts/render_limpiar_bd.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiparking.settings')

# En Render, el directorio de trabajo puede no ser la raíz del proyecto
# Asegurar que el path del proyecto esté en sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

django.setup()

from cupones.models import Cupon, CuponAplicado
from reservas.models import Reserva
from pagos.models import Pago
from parqueadero.models import InventarioParqueo, Espacio, TipoEspacio, Piso
from vehiculos.models import Vehiculo
from tarifas.models import Tarifa
from usuarios.models import Usuario

print("=" * 60)
print("  LIMPIEZA DE BASE DE DATOS - MultiParking (Render)")
print("=" * 60)

# Orden de eliminación: primero las tablas dependientes
tablas = [
    ("Cupones Aplicados", CuponAplicado),
    ("Cupones", Cupon),
    ("Reservas", Reserva),
    ("Pagos", Pago),
    ("Inventario Parqueo", InventarioParqueo),
    ("Espacios", Espacio),
    ("Tarifas", Tarifa),
    ("Tipos de Espacio", TipoEspacio),
    ("Pisos", Piso),
    ("Vehiculos", Vehiculo),
    ("Usuarios", Usuario),
]

total_eliminados = 0

for nombre, modelo in tablas:
    count = modelo.objects.count()
    if count > 0:
        modelo.objects.all().delete()
        print(f"  [OK] {nombre}: {count} registros eliminados")
        total_eliminados += count
    else:
        print(f"  [--] {nombre}: sin registros")

print("\n" + "=" * 60)
print(f"  LIMPIEZA COMPLETADA - {total_eliminados} registros eliminados")
print("=" * 60)
print("\nPara cargar datos de prueba ejecuta:")
print("  python scripts/render_datos_prueba.py")
