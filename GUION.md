# Guión de Presentación — MultiParking

**Fecha:** Lunes 11 de Mayo
**Tiempo total:** ~11 minutos

---

## ⏱ Distribución de Tiempo

| Punto | Contenido | Tiempo | Diapositiva |
|-------|-----------|--------|-------------|
| 1 | Presentación integrantes | 0:15 | Diap. 1 |
| 2 | Necesidad encontrada | 1:00 | Diap. 2 |
| 3 | Resumen del proyecto | 2:00 | Diap. 3 y 4 |
| 4a | Patrón de diseño | 0:20 | Diap. 5 |
| 4b | Lenguajes de programación | 0:20 | Diap. 6 |
| 4c | Frameworks | — | (misma diap. 6) |
| 4d | Base de datos | 0:20 | Diap. 7 |
| 5 | Prototipo funcional | 3:00 | Diap. 8 + Demo viva |
| 6 | Explicación del código | 3:00 | Diap. 10 y 11 |
| — | Cierre | 0:15 | Diap. 12 |
| **Total** | | **~11 min** | |

---

## 📋 Guión Completo

---

### PUNTO 1 — Presentación del grupo (0:15)
*Diapositiva 1*

> Presentar cada integrante con nombre. Ser breve — 15 segundos.

**[Integrante 1]:** "Buenos días / tardes. Mi nombre es ___, desarrollé ___"
**[Integrante 2]:** "Soy ___, me encargué de ___"
*(repetir para cada integrante)*

---

### PUNTO 2 — La necesidad encontrada (1:00)
*Diapositiva 2*

> Abrir con el problema real. Hacer que suene cotidiano.

*"Los parqueaderos de Colombia, especialmente los multinivel, manejan hoy su operación con métodos manuales: cuadernos, Excel, o simplemente contando espacios a ojo. Esto genera filas en la entrada, errores en el cobro, sin historial de quién entró ni cuándo, y sin posibilidad de reservar un espacio antes de llegar.*

*Esta situación la pudimos observar de primera mano, y fue la necesidad que nos motivó a construir MultiParking."*

> 👉 **Referencia GitHub:** *"Como pueden ver aquí en el README de nuestro proyecto —* `github.com/xeodeo/Multiparking-Django` *— en la sección 'Descripción', listamos los casos de uso reales donde esto aplica."*

---

### PUNTO 3 — Resumen del proyecto (2:00)
*Diapositivas 3 y 4*

> Dar la visión general rápido, luego mostrar los 3 paneles.

*"MultiParking es una aplicación web que digitaliza completamente la operación de un parqueadero multinivel. Tiene tres roles principales: el administrador que configura y supervisa todo, el vigilante o guardia que opera en tiempo real, y el cliente que puede reservar, pagar y gestionar sus vehículos desde el celular.*

*Ya está desplegada en producción en Render.com y pueden acceder ahorita mismo en multiparking-django.onrender.com."*

> 👉 **Referencia GitHub:** *"En la sección 'Características' del README encontrarán el detalle completo de cada panel."*

---

### PUNTO 4 — Explicación del software (1:00 total)
*Diapositivas 5, 6 y 7*

#### 4a — Patrón de diseño (0:20)
*Diapositiva 5*

*"El proyecto aplica el patrón MVT — Model, View, Template — que es el patrón propio de Django. El modelo define los datos y las reglas de negocio, la vista maneja la lógica y el control de acceso por rol, y el template genera el HTML que ve el usuario. Adicionalmente usamos un middleware chain para manejar seguridad y errores de base de datos."*

> 👉 **Referencia GitHub:** *"Está documentado en la sección 'Patrón de Diseño' del README."*

#### 4b y 4c — Lenguajes y Frameworks (0:20)
*Diapositiva 6*

*"El backend está en Python 3.12 con Django. El frontend usa Tailwind CSS con los templates de Django — renderizado del lado del servidor. Para gráficos usamos Chart.js, y para los reportes ReportLab para PDF y openpyxl para Excel."*

> 👉 **Referencia GitHub:** *"La tabla de tecnologías está en la sección 'Tecnologías' del README."*

#### 4d — Base de datos (0:20)
*Diapositiva 7*

*"En desarrollo usamos MySQL 8.0 y en producción PostgreSQL en Render.com. Tenemos 10 tablas principales conectadas mediante el ORM de Django — sin SQL manual. Los modelos siguen una convención de nomenclatura en camelCase con prefijo de tabla."*

> 👉 **Referencia GitHub:** *"Las convenciones de naming están en 'Convenciones del Código' en el README."*

---

### PUNTO 5 — Prototipo funcional (3:00)
*Diapositiva 8 → pantalla completa de la demo*

> ⚠️ Tener la demo abierta ANTES de la presentación. El cold start de Render tarda 30-50 segundos.

**0:00–0:30** — Diapositiva 8: presentar credenciales y URL

*"Vamos a mostrar el sistema en vivo. Está desplegado en Render.com con PostgreSQL."*

> 👉 **Referencia GitHub:** *"Las credenciales de acceso están en la sección 'Demo en Vivo' del README."*

**0:30–1:00** — Iniciar sesión como admin. Mostrar dashboard.

*"Este es el panel del administrador. Vemos las estadísticas en tiempo real — espacios ocupados, ingresos de los últimos 7 días en el gráfico, y el mapa de pisos donde cada cuadrito es un espacio."*

**1:00–1:30** — Ir a Guardia. Mostrar registrar ingreso.

*"Ahora el panel del guardia. Desde acá se registra la entrada de un vehículo buscando por placa, se asigna el espacio disponible, y queda en el sistema."*

**1:30–2:00** — Registrar salida. Mostrar cálculo automático y recibo.

*"Al registrar la salida, el sistema calcula automáticamente el cobro según la tarifa activa y el tiempo de estadía. Se puede generar un recibo imprimible."*

**2:00–2:30** — Iniciar sesión como cliente. Mostrar reservas y stickers.

*"El cliente tiene su propio panel donde puede reservar espacios, ver sus vehículos y el programa de fidelidad — acumula stickers por cada parqueo y al llegar a la meta obtiene un cupón de descuento."*

**2:30–3:00** — Mostrar reporte PDF desde el panel admin.

*"Y finalmente, el administrador puede exportar reportes en PDF o Excel con el historial completo de pagos."*

---

### PUNTO 6 — Explicación del código (3:00)
*Diapositivas 10 y 11*

**0:00–1:00** — Diapositiva 10: intérprete

*"Python es un lenguaje interpretado. Esto significa que el código no se compila a binario antes de ejecutarse — el intérprete CPython lee y ejecuta el código línea por línea. En la práctica para MultiParking, cuando llega una solicitud HTTP, Gunicorn la recibe, Django la procesa en Python, consulta a PostgreSQL mediante el ORM, y devuelve el HTML renderizado. No necesita paso de compilación — lo que vimos funcionando en la demo corrió exactamente así."*

**1:00–2:00** — Diapositiva 11: estructura del código

*"El código está organizado en 10 apps Django independientes, cada una con su modelo, sus vistas y sus templates. Por ejemplo, la lógica de cobro está en pagos/views.py, el cálculo de ocupación de pisos en parqueadero/utils.py, y toda la seguridad en el middleware de multiparking/middleware.py. Tenemos aproximadamente 40 vistas, 15 modelos y 60 templates."*

> 👉 **Referencia GitHub:** *"Pueden ver la estructura completa de archivos en 'Estructura del Proyecto' del README, y el script de despliegue en el archivo `build.sh` en la raíz del repositorio."*

**2:00–3:00** — Mostrar brevemente un archivo de código (opcional)

> Abrir en GitHub: `parqueadero/utils.py` o `pagos/views.py` para mostrar un fragmento real.

*"Por ejemplo, aquí en utils.py está el cálculo que muestra los pisos. Se puede ver cómo se usan los modelos del ORM, el prefetch para optimizar consultas, y cómo se inyectan atributos calculados para usarlos directamente en el template."*

---

### CIERRE (0:15)
*Diapositiva 12*

*"MultiParking pasó de ser un problema real identificado a un sistema funcional en producción. El código está público en GitHub y la demo está disponible ahora mismo. Gracias."*

---

## 🔗 Links para tener abiertos antes de empezar

1. **Demo:** https://multiparking-django.onrender.com *(abrir 2 minutos antes para el cold start)*
2. **README:** https://github.com/xeodeo/Multiparking-Django#características
3. **Código fuente:** https://github.com/xeodeo/Multiparking-Django
4. **build.sh:** https://github.com/xeodeo/Multiparking-Django/blob/main/build.sh

---

## ⚡ Tips para la demo en vivo

- Iniciar sesión como **admin** primero — tiene el recorrido más completo
- Si el sistema está lento (cold start), mencionar que es el plan gratuito de Render
- Si algo falla, mostrar capturas de pantalla como respaldo
- Tener las credenciales visibles (están en la diapositiva 8)
