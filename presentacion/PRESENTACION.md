# Presentación MultiParking — Lunes 11 de Mayo

> **Referencia GitHub:** https://github.com/xeodeo/Multiparking-Django
> **Demo en vivo:** https://multiparking-django.onrender.com

---

## DIAPOSITIVA 1 — Portada
**[15 segundos · Punto 1: Integrantes]**

```
MultiParking
Sistema de Gestión de Parqueaderos

Kevin Ovalle · Kevin Santiago Pinto López
Mayo 2025
```

> *Sin referencia a README — solo presentar cada integrante con nombre y rol en el equipo.*

---

## DIAPOSITIVA 2 — La Necesidad
**[1 minuto · Punto 2: Situación actual del cliente]**

```
El Problema

Observado en un parqueadero real en Suba, Bogotá:
  • Control manual en papel o Excel, sin visibilidad en tiempo real
  • Cobros calculados a mano → errores y demoras en la salida
  • Sin historial de vehículos ni trazabilidad de incidentes
  • Sin posibilidad de reservar un espacio antes de llegar

Resultado: pérdida de ingresos, filas en la entrada
y experiencia deficiente para el cliente.
```

> *Aquí puedes señalar: "Esta necesidad la documentamos en la sección **Descripción > Casos de Uso** del README del proyecto"*
> **README → sección "Descripción / Casos de Uso"**

---

## DIAPOSITIVA 3 — ¿Qué es MultiParking?
**[1 minuto · Punto 3: Resumen del proyecto — parte 1]**

```
MultiParking

Aplicación web para la gestión completa
de parqueaderos.

✓ Control de espacios en tiempo real
✓ 3 roles: Administrador · Vigilante · Cliente
✓ Entrada y salida con cálculo automático de cobro
✓ Reservas online desde el celular
✓ Reportes y estadísticas exportables
✓ Desplegado en producción (Render.com)

Demo: multiparking-django.onrender.com
```

> *"Pueden ver el resumen completo en la sección **Características** del README"*
> **README → sección "Características"**

---

## DIAPOSITIVA 4 — Los 3 Paneles
**[1 minuto · Punto 3: Resumen del proyecto — parte 2]**

```
Tres perfiles, tres experiencias

ADMINISTRADOR              VIGILANTE (Guardia)       CLIENTE
─────────────────────      ──────────────────────    ──────────────────
Dashboard con gráficos     Registra ingreso/salida   Reserva espacios
Gestiona espacios/pisos    Confirma pagos efectivo   Ve sus vehículos
Configura tarifas          Ve ocupación en vivo      Acumula stickers
Exporta reportes PDF/Excel Genera recibo al salir    Canjea descuentos
Gestiona usuarios          ─────────────────────     Salida por QR
```

> *Mostrar en vivo: iniciar sesión como admin en la demo*
> **README → sección "Panel de Administración / Panel Guardia / Panel Cliente"**

---

## DIAPOSITIVA 5 — Patrón de Diseño
**[~20 seg · Punto 4a: Patrón de diseño]**

```
Patrón MVT (Model – View – Template)

MODEL   → Modelos Django con validaciones y reglas de negocio
VIEW    → Class-Based Views con mixins de autorización por rol
TEMPLATE→ Server-Side Rendering con Tailwind CSS

+ Middleware chain para seguridad y manejo de errores
+ Singleton pattern en Configuración de Fidelidad
+ Separación por apps independientes (10 módulos)
```

> *"La arquitectura está documentada en **Patrón de Diseño** del README"*
> **README → sección "Patrón de Diseño"**

---

## DIAPOSITIVA 6 — Lenguajes y Frameworks
**[~20 seg · Punto 4b y 4c: Lenguajes + Frameworks]**

```
Stack Tecnológico

BACKEND               FRONTEND              HERRAMIENTAS
────────────────       ──────────────────    ──────────────
Python 3.12+           Tailwind CSS (CDN)    Git + GitHub
Django 5.x             Django Templates      Render.com
Django REST Framework  Chart.js              Gunicorn
                       HTML5 / JavaScript    WhiteNoise
```

> *"La tabla completa está en la sección **Tecnologías** del README"*
> **README → sección "Tecnologías"**

---

## DIAPOSITIVA 7 — Base de Datos
**[~20 seg · Punto 4d: Base de datos]**

```
Base de Datos

Desarrollo    →  MySQL 8.0 (utf8mb4)
Producción    →  PostgreSQL (Render.com)

10 tablas principales:
usuarios · vehiculos · espacios · inventario_parqueo
pagos · cupones · reservas · novedades
fidelidad_configuracion · fidelidad_stickers

ORM Django — sin SQL manual
Migraciones versionadas con makemigrations
```

> *"Las convenciones de nomenclatura están en **Convenciones del Código** del README"*
> **README → sección "Convenciones del Código"**

---

## DIAPOSITIVA 8 — Demo en Vivo (intro)
**[30 seg · Punto 5: Prototipo funcional — presentación]**

```
Prototipo Funcional

🌐 multiparking-django.onrender.com

Desplegado en Render.com con:
  • PostgreSQL como base de datos en producción
  • Gunicorn como servidor WSGI
  • WhiteNoise para archivos estáticos

Credenciales:
  Admin     →  admin@multiparking.com   /  admin123
  Vigilante →  vigilante@multiparking.com / vigil123
  Cliente   →  cliente@test.com          / test123
```

> *"Las credenciales completas y cupones activos están al final del README, sección **Demo en Vivo**"*
> **README → sección "Demo en Vivo / Credenciales de Prueba"**

---

## DIAPOSITIVA 9 — Demo en Vivo (mostrar)
**[2.5 minutos · Punto 5: recorrido de la demo]**

```
Recorrido del Sistema

1. Página de inicio pública
2. Panel Admin → Dashboard con gráficos en tiempo real
3. Vista General de Pisos → mapa de espacios
4. Registrar entrada de un vehículo (guardia)
5. Registrar salida + recibo imprimible
6. Panel Cliente → reservas y programa de fidelidad
7. Reportes → exportar PDF
```

> *Navegar en vivo por la demo. No hay diapositiva aquí — es pantalla completa del sistema.*

---

## DIAPOSITIVA 10 — El Código: Intérprete
**[1 minuto · Punto 6: Compilador o intérprete]**

```
Python es un lenguaje INTERPRETADO

El código fuente (.py) es ejecutado línea por línea
por el intérprete CPython — no se compila a binario.

Ciclo en MultiParking:
  1. Solicitud HTTP llega a Gunicorn
  2. Django (Python) interpreta y procesa la vista
  3. Consulta a PostgreSQL vía ORM
  4. Template renderizado → HTML de vuelta al navegador

No necesita compilación previa → desarrollo más ágil,
despliegue inmediato en Render con `build.sh`
```

> *"El script de despliegue está en `build.sh` en la raíz del repositorio"*
> **GitHub → archivo `build.sh` en la raíz**

---

## DIAPOSITIVA 11 — El Código: estructura
**[1 minuto · Punto 6: Explicación del código]**

```
Estructura del Código

Cada funcionalidad es una app Django independiente:

  pagos/views.py     →  lógica de cobro y recibos
  parqueadero/utils.py → cálculo de ocupación de pisos
  multiparking/middleware.py → seguridad y errores

Ejemplo de regla de negocio en código:
  monto = ceil((minutos / 60) * precioHora / 100) * 100
  (redondeo hacia arriba a los 100 COP más cercanos)

10 apps · ~40 vistas · ~15 modelos · ~60 templates
```

> *"La arquitectura completa de apps está en **Estructura del Proyecto** del README"*
> **README → sección "Estructura del Proyecto" / "Arquitectura de Apps"**

---

## DIAPOSITIVA 12 — Cierre
**[15 seg · Cierre]**

```
MultiParking

Problema real → Solución funcional en producción

GitHub:  github.com/xeodeo/Multiparking-Django
Demo:    multiparking-django.onrender.com

¿Preguntas?
```
