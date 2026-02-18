# Solución: Gráfica de Ingresos Últimos 7 Días

## Problema Identificado

La gráfica "Ingresos Últimos 7 Días" en el dashboard dejaba de funcionar después de apagar el servidor, causando que no se mostraran datos.

### Causas Raíz

1. **Borrado automático de datos**: El script `generar_datos_prueba.py` borraba todos los pagos en las líneas 109-110 cada vez que se ejecutaba

2. **Problema con timezones en MySQL**: El filtro `pagFechaPago__date__gte` y `pagFechaPago__date__lte` no funcionaba correctamente con zonas horarias en MySQL, retornando 0 resultados aunque existieran pagos válidos

3. **Campos auto_now_add**: Los campos `parHoraEntrada` y `pagFechaPago` tienen `auto_now_add=True`, lo que ignoraba las fechas personalizadas para datos de prueba

## Soluciones Implementadas

### 1. Scripts Mejorados

#### `mantener_datos_demo.py` (NUEVO)
Script principal para mantener datos de demostración siempre actualizados:
- ✅ **NO borra** datos existentes
- ✅ Verifica si hay suficientes pagos recientes (mínimo 14)
- ✅ Genera pagos distribuidos en los últimos 5 días
- ✅ Limpia automáticamente pagos muy antiguos (+30 días)
- ✅ Muestra distribución por día y total de ingresos
- ✅ Usa el método correcto de filtrado con `__range`

```bash
python mantener_datos_demo.py
```

#### `cargar_datos_iniciales.py` (NUEVO)
Carga la estructura base de datos necesaria:
- Crea usuarios admin y cliente de prueba
- Crea pisos, tipos de espacios, espacios de parqueo
- Configura tarifas activas
- Registra vehículos de prueba

```bash
python cargar_datos_iniciales.py
```

#### `generar_datos_prueba.py` (MODIFICADO)
- ✅ Ya NO borra todos los pagos automáticamente
- ✅ Verifica si ya existen datos antes de generar
- ✅ Usa el método correcto para crear fechas personalizadas

### 2. Corrección en Código de Producción

#### `parqueadero/views.py` (Líneas 51-60)
**Antes:**
```python
pagos_semana = Pago.objects.filter(
    pagFechaPago__date__gte=hace_7_dias,  # ❌ No funciona con MySQL + timezones
    pagFechaPago__date__lte=hoy_local,
    pagEstado='PAGADO',
)
```

**Después:**
```python
from datetime import datetime
inicio_rango = timezone.make_aware(datetime.combine(hace_7_dias, datetime.min.time()))
fin_rango = timezone.make_aware(datetime.combine(hoy_local, datetime.max.time()))

pagos_semana = Pago.objects.filter(
    pagFechaPago__range=(inicio_rango, fin_rango),  # ✅ Funciona correctamente
    pagEstado='PAGADO',
)
```

#### `check_pagos.py` (ACTUALIZADO)
Actualizado para usar el mismo método de filtrado correcto.

### 3. Solución para auto_now_add

Para generar datos de prueba con fechas personalizadas, se usa el patrón:

```python
# Crear el objeto
pago = Pago.objects.create(
    pagMonto=monto,
    pagMetodo='EFECTIVO',
    pagEstado='PAGADO',
    fkIdParqueo=registro,
)

# Actualizar el campo auto_now_add manualmente
Pago.objects.filter(pk=pago.pk).update(pagFechaPago=fecha_personalizada)
```

### 4. Automatización (Opcional)

#### `ejecutar_mantenimiento.bat` (NUEVO)
Script de Windows para ejecutar el mantenimiento fácilmente:
```batch
@echo off
cd /d "%~dp0"
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python mantener_datos_demo.py
pause
```

## Uso Recomendado

### Primera Vez (Configuración Inicial)
```bash
# 1. Cargar estructura base
python cargar_datos_iniciales.py

# 2. Generar pagos de demostración
python mantener_datos_demo.py

# 3. Verificar que funciona
python check_pagos.py
```

### Uso Diario

**Opción 1: Manual**
```bash
# Ejecutar antes de iniciar el servidor
python mantener_datos_demo.py
python manage.py runserver
```

**Opción 2: Script combinado**
```bash
# Usar el archivo BAT
ejecutar_mantenimiento.bat
```

**Opción 3: Automatizado**
Programar `ejecutar_mantenimiento.bat` en el Programador de Tareas de Windows para que se ejecute diariamente a medianoche.

## Resultado

✅ Los datos ahora persisten correctamente en MySQL
✅ La gráfica muestra datos distribuidos en los últimos 7 días
✅ Los pagos se generan con fechas realistas (diferentes días y horas)
✅ El mantenimiento automático asegura que siempre haya datos recientes
✅ No se requiere regenerar datos manualmente después de cada reinicio

## Ejemplo de Salida

```
============================================================
>> Mantenimiento de Datos de Demostracion
============================================================

[INFO] Fecha actual: 2026-02-17
[INFO] Rango de busqueda: 2026-02-11 a 2026-02-17
[INFO] Pagos en ultimos 7 dias: 15

[OK] Hay suficientes pagos recientes. No se requiere accion.

============================================================
>> RESUMEN
============================================================
Pagos en ultimos 7 dias: 15
Total pagos en sistema: 15
Total inventario: 15
Ingresos ultimos 7 dias: $225,000

Distribucion por dia:
  2026-02-17: 3 pagos - $45,000
  2026-02-16: 3 pagos - $45,000
  2026-02-15: 3 pagos - $45,000
  2026-02-14: 3 pagos - $45,000
  2026-02-13: 3 pagos - $45,000

[OK] Mantenimiento completado!
```

## Archivos Creados/Modificados

### Nuevos
- `mantener_datos_demo.py` - Script de mantenimiento automático
- `cargar_datos_iniciales.py` - Carga estructura base
- `ejecutar_mantenimiento.bat` - Script de Windows para automatización
- `DATOS_DEMO.md` - Guía detallada
- `SOLUCION_GRAFICA.md` - Este documento

### Modificados
- `generar_datos_prueba.py` - Eliminado borrado automático, corregidos campos auto_now_add
- `parqueadero/views.py` - Corregido filtro de fechas con __range
- `check_pagos.py` - Actualizado con filtro correcto
- `mantener_datos_demo.py` - Corregidos filtros y campos auto_now_add

## Credenciales de Prueba

```
Admin:
Email: admin@multiparking.com
Contraseña: admin123

Cliente:
Email: cliente@test.com
Contraseña: test123
```

## Soporte

Para más detalles, consulta: [DATOS_DEMO.md](./DATOS_DEMO.md)
