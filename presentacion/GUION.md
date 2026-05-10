# Guión de Presentación — MultiParking

**Fecha:** Lunes 11 de Mayo
**Tiempo total:** ~11 minutos

---

## 👥 División por Integrante

| Integrante | Diapositivas | Tiempo aprox. | Tipo |
|---|---|---|---|
| **Kevin Ovalle** | 1 · 2 · 3 · 4 · 12 | ~3:30 min | Contexto y negocio (las más fáciles) |
| **Kevin Santiago Pinto López** | 5 · 6 · 7 · 8 · 9 · 10 · 11 | ~7:00 min | Técnicas + demo en vivo |

### Orden de turnos en la presentación

```
Kevin Ovalle       →  Diap. 1–4    (intro, problema, qué es, 3 paneles)
Kevin Santiago     →  Diap. 5–11   (MVT, stack, BD, demo, intérprete, código)
Kevin Ovalle       →  Diap. 12     (cierre)
```

---

## ⏱ Distribución de Tiempo

| Diap. | Contenido | Tiempo | Quién |
|-------|-----------|--------|-------|
| 1 | Presentación integrantes | 0:15 | **Ovalle** |
| 2 | Necesidad encontrada | 1:00 | **Ovalle** |
| 3 | Qué es MultiParking | 1:00 | **Ovalle** |
| 4 | Los 3 paneles | 1:00 | **Ovalle** |
| 5 | Patrón de diseño MVT | 0:20 | **Santiago** |
| 6 | Lenguajes y frameworks | 0:20 | **Santiago** |
| 7 | Base de datos | 0:20 | **Santiago** |
| 8 | Demo — credenciales | 0:30 | **Santiago** |
| 9 | Demo — recorrido en vivo | 2:30 | **Santiago** |
| 10 | Python: intérprete | 1:00 | **Santiago** |
| 11 | Estructura del código | 1:00 | **Santiago** |
| 12 | Cierre | 0:15 | **Ovalle** |
| **Total** | | **~11 min** | |

---

## 📋 Guión Completo

---

### 🟢 KEVIN OVALLE — Diapositiva 1 (0:15)

> Solo habla Kevin Ovalle. Breve y directo.

**Kevin Ovalle:** *"Buenos días. Nuestro equipo está conformado por Kevin Ovalle y Kevin Santiago Pinto López. Hoy les presentamos MultiParking — un sistema de gestión de parqueaderos. Partimos del análisis de un parqueadero real en la localidad de Suba, y construimos una solución que puede expandirse a centros comerciales, hoteles, edificios corporativos y universidades."*

---

### 🟢 KEVIN OVALLE — Diapositiva 2 · La necesidad (1:00)

> Abrir con el problema real. Hacer que suene cotidiano.

*"Los parqueaderos en Colombia manejan hoy su operación con métodos manuales: cuadernos, Excel, o simplemente contando espacios a ojo. Esto genera filas en la entrada, errores en el cobro, sin historial de quién entró ni cuándo, y sin posibilidad de reservar un espacio antes de llegar.*

*Esta situación la pudimos observar de primera mano, y fue la necesidad que nos motivó a construir MultiParking."*

> 👉 **GitHub:** sección *Descripción / Casos de Uso* del README

---

### 🟢 KEVIN OVALLE — Diapositivas 3 y 4 · Resumen del proyecto (2:00)

> Dar la visión general rápido, luego mostrar los 3 paneles.

*"MultiParking es una aplicación web que digitaliza completamente la operación de un parqueadero. Tiene tres roles principales: el administrador que configura y supervisa todo, el vigilante que opera en tiempo real, y el cliente que puede reservar, pagar y gestionar sus vehículos desde el celular.*

*Ya está desplegada en producción en Render.com y pueden acceder ahorita mismo en multiparking-django.onrender.com."*

> 👉 **GitHub:** sección *Características* del README

---

### 🔵 KEVIN SANTIAGO — Diapositiva 5 · Patrón MVT (0:20)

*"El proyecto aplica el patrón MVT — Model, View, Template — que es el patrón propio de Django. El modelo define los datos y las reglas de negocio, la vista maneja la lógica y el control de acceso por rol, y el template genera el HTML que ve el usuario. Adicionalmente usamos un middleware chain para seguridad y manejo de errores de base de datos."*

> 👉 **GitHub:** sección *Patrón de Diseño* del README

---

### 🔵 KEVIN SANTIAGO — Diapositiva 6 · Stack tecnológico (0:20)

*"El backend está en Python 3.12 con Django. El frontend usa Tailwind CSS con los templates de Django — renderizado del lado del servidor. Para gráficos usamos Chart.js, y para los reportes ReportLab para PDF y openpyxl para Excel."*

> 👉 **GitHub:** sección *Tecnologías* del README

---

### 🔵 KEVIN SANTIAGO — Diapositiva 7 · Base de datos (0:20)

*"En desarrollo usamos MySQL 8.0 y en producción PostgreSQL en Render.com. Tenemos 10 tablas principales conectadas mediante el ORM de Django — sin SQL manual."*

> 👉 **GitHub:** sección *Convenciones del Código* del README

---

### 🔵 KEVIN SANTIAGO — Diapositiva 8 · Demo intro (0:30)

> ⚠️ Tener la demo abierta ANTES de la presentación. El cold start tarda 30–50 segundos.

*"Vamos a mostrar el sistema en vivo. Está desplegado en Render.com con PostgreSQL."*

> 👉 **GitHub:** sección *Demo en Vivo / Credenciales de Prueba* del README

---

### 🔵 KEVIN SANTIAGO — Diapositiva 9 · Recorrido demo (2:30)

**0:00–0:30** — Iniciar sesión como admin. Mostrar dashboard.

*"Este es el panel del administrador. Vemos las estadísticas en tiempo real — espacios ocupados, ingresos de los últimos 7 días, y el mapa de pisos."*

**0:30–1:00** — Ir a Guardia. Registrar ingreso.

*"El panel del guardia. Se registra la entrada buscando por placa y se asigna el espacio disponible."*

**1:00–1:30** — Registrar salida. Cálculo automático y recibo.

*"Al registrar la salida, el sistema calcula automáticamente el cobro y genera un recibo imprimible."*

**1:30–2:00** — Panel cliente. Reservas y stickers.

*"El cliente puede reservar espacios y acumula stickers por cada parqueo — al llegar a la meta obtiene un cupón de descuento."*

**2:00–2:30** — Reporte PDF desde admin.

*"El administrador puede exportar reportes en PDF o Excel con el historial completo de pagos."*

---

### 🔵 KEVIN SANTIAGO — Diapositiva 10 · Intérprete (1:00)

*"Python es un lenguaje interpretado. Esto significa que el código no se compila a binario — el intérprete CPython ejecuta línea por línea. En MultiParking: Gunicorn recibe la petición, Django la procesa, consulta a PostgreSQL mediante el ORM, y devuelve el HTML. Sin paso de compilación — el despliegue en Render es inmediato con build.sh."*

> 👉 **GitHub:** archivo `build.sh` en la raíz

---

### 🔵 KEVIN SANTIAGO — Diapositiva 11 · Estructura del código (1:00)

*"El código está organizado en 10 apps Django independientes. La lógica de cobro está en pagos/views.py, el cálculo de ocupación en parqueadero/utils.py, y la seguridad en multiparking/middleware.py. Aproximadamente 40 vistas, 15 modelos y 60 templates."*

> 👉 **GitHub:** sección *Estructura del Proyecto* del README

---

### 🟢 KEVIN OVALLE — Diapositiva 12 · Cierre (0:15)

*"MultiParking pasó de ser un problema real identificado a un sistema funcional en producción. El código está público en GitHub y la demo está disponible ahora mismo. Gracias."*

---

## 🔗 Links para tener abiertos antes de empezar

1. **Demo:** https://multiparking-django.onrender.com *(abrir 2 min antes para cold start)*
2. **README:** https://github.com/xeodeo/Multiparking-Django
3. **build.sh:** https://github.com/xeodeo/Multiparking-Django/blob/main/build.sh

---

## ⚡ Tips

- Abrir la demo **2 minutos antes** — cold start de Render tarda 30–50 seg
- Si el sistema está lento, mencionarlo: *"es el plan gratuito de Render"*
- Credenciales visibles en diapositiva 8
- Kevin Ovalle puede relajarse mientras Kevin Santiago hace la demo y el código
