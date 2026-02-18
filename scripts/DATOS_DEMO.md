# Guía de Datos de Demostración

Este documento explica cómo mantener datos de demostración persistentes en el sistema MultiParking, asegurando que la gráfica "Ingresos Últimos 7 Días" siempre muestre datos.

## Problema Identificado

Los datos de la gráfica desaparecían porque:
1. El script `generar_datos_prueba.py` borraba todos los pagos cada vez que se ejecutaba
2. Los pagos se generaban con fechas relativas, quedando "antiguos" después de varios días

## Solución Implementada

Se crearon 3 scripts complementarios para mantener datos persistentes:

### 1. `cargar_datos_iniciales.py`
**Propósito:** Crear la estructura base de datos (usuarios, pisos, espacios, tarifas, vehículos)

**Cuándo usar:** Primera vez que configuras el sistema o después de resetear la base de datos

```bash
python cargar_datos_iniciales.py
```

**Crea:**
- 2 usuarios: admin@multiparking.com y cliente@test.com
- 3 pisos
- 3 tipos de espacios (Estándar, Moto, VIP)
- 30 espacios de parqueo
- 2 tarifas activas
- 5 vehículos de prueba

### 2. `mantener_datos_demo.py`
**Propósito:** Mantener pagos siempre actualizados en los últimos 7 días

**Cuándo usar:** Ejecutar diariamente o cuando notes que faltan datos en la gráfica

```bash
python mantener_datos_demo.py
```

**Funciones:**
- Verifica pagos en los últimos 7 días
- Si hay menos de 14 pagos, genera más automáticamente
- Limpia pagos muy antiguos (más de 30 días)
- Muestra distribución de ingresos por día

### 3. `generar_datos_prueba.py` (Modificado)
**Propósito:** Generar datos de prueba iniciales SIN borrar datos existentes

**Cambios realizados:**
- ❌ YA NO borra pagos anteriores
- ✅ Verifica si ya hay datos recientes
- ✅ Solo genera si es necesario

```bash
python generar_datos_prueba.py
```

## Configuración Recomendada

### Opción 1: Ejecución Manual
Ejecuta `mantener_datos_demo.py` cada vez que inicies el servidor o notes que faltan datos:

```bash
python mantener_datos_demo.py
python manage.py runserver
```

### Opción 2: Automatización con Programador de Tareas de Windows

1. **Ejecutar el archivo BAT:**
   - Haz doble clic en `ejecutar_mantenimiento.bat`
   - O ejecútalo desde línea de comandos

2. **Programar ejecución automática diaria:**

   a) Abre el Programador de tareas de Windows:
      - Presiona `Win + R`
      - Escribe `taskschd.msc`
      - Presiona Enter

   b) Crear nueva tarea:
      - Clic en "Crear tarea básica"
      - Nombre: "MultiParking - Mantener Datos Demo"
      - Descripción: "Actualiza datos de demostración diariamente"

   c) Configurar desencadenador:
      - Frecuencia: Diariamente
      - Hora: 00:00 (medianoche) o la que prefieras

   d) Configurar acción:
      - Acción: "Iniciar un programa"
      - Programa: Buscar `ejecutar_mantenimiento.bat`
      - Directorio: `C:\Users\xeodeo\Desktop\Gemini - copia`

   e) Guardar la tarea

### Opción 3: Ejecutar al Iniciar Servidor (Más Simple)

Crea un script combinado `iniciar_servidor.bat`:

```batch
@echo off
echo Actualizando datos de demostracion...
python mantener_datos_demo.py

echo.
echo Iniciando servidor Django...
python manage.py runserver
```

## Verificación

Para verificar que los datos están correctos:

```bash
python check_pagos.py
```

Este script muestra:
- Total de pagos en la base de datos
- Pagos en los últimos 7 días
- Distribución por fecha
- Rango de búsqueda de la gráfica

## Flujo de Trabajo Recomendado

### Primera vez (Configuración inicial)
```bash
# 1. Crear estructura base
python cargar_datos_iniciales.py

# 2. Generar pagos de demostración
python mantener_datos_demo.py

# 3. Verificar
python check_pagos.py

# 4. Iniciar servidor
python manage.py runserver
```

### Uso diario
```bash
# Ejecutar antes de iniciar el servidor
python mantener_datos_demo.py && python manage.py runserver
```

O simplemente:
```bash
# Usar el script BAT
ejecutar_mantenimiento.bat
```

## Notas Importantes

1. **Base de datos MySQL:** Los datos se guardan en MySQL y persisten entre reinicios del servidor

2. **Limpieza automática:** `mantener_datos_demo.py` elimina pagos de más de 30 días para evitar acumulación excesiva

3. **Sin interferencia con datos reales:** Los scripts solo crean/modifican datos de prueba (con `pagMetodo='EFECTIVO'`)

4. **Datos realistas:** Se generan 2-3 pagos por día con montos y horarios variables

## Solución de Problemas

### La gráfica sigue vacía
```bash
# Verificar pagos en BD
python check_pagos.py

# Si no hay pagos, generar
python mantener_datos_demo.py

# Verificar nuevamente
python check_pagos.py
```

### Error: "Faltan datos básicos"
```bash
# Cargar datos iniciales primero
python cargar_datos_iniciales.py

# Luego generar pagos
python mantener_datos_demo.py
```

### Muchos datos antiguos
```bash
# El script limpia automáticamente, pero puedes forzar limpieza:
# (Ejecutar en shell de Django)
python manage.py shell

# En el shell:
from pagos.models import Pago
from datetime import datetime, timedelta
hace_30_dias = datetime.now() - timedelta(days=30)
Pago.objects.filter(pagFechaPago__lt=hace_30_dias, pagMetodo='EFECTIVO').delete()
```

## Archivos Relacionados

- `cargar_datos_iniciales.py` - Carga estructura base
- `mantener_datos_demo.py` - Mantiene pagos actualizados
- `generar_datos_prueba.py` - Genera datos iniciales (modificado para no borrar)
- `ejecutar_mantenimiento.bat` - Script de Windows para automatización
- `check_pagos.py` - Verificación de datos
- `DATOS_DEMO.md` - Esta guía

## Credenciales de Prueba

```
Admin:
Email: admin@multiparking.com
Contraseña: admin123

Cliente:
Email: cliente@test.com
Contraseña: test123
```
