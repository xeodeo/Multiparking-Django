# MultiParking

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0_dev-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-producción-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CDN-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Sistema de gestión inteligente para parqueaderos**

[Demo en Vivo](https://multiparking-django.onrender.com) · [Instalación](#-instalación) · [Características](#-características) · [Credenciales de prueba](#demo-en-vivo)

</div>

---

## Descripción

**MultiParking** es una aplicación web desarrollada en Django para la administración completa de parqueaderos. Nació del análisis de un parqueadero real en la localidad de Suba, Bogotá, y fue diseñada para escalar a cualquier tipo de establecimiento que necesite gestionar espacios de parqueo, vehículos, reservas, tarifas, pagos, cupones de descuento, novedades e incidentes, y un programa de fidelidad con stickers.

### Casos de Uso

- **Origen:** parqueadero en Suba, Bogotá — caso de análisis real
- Centros comerciales con control de acceso vehicular y reservas anticipadas
- Hoteles con gestión de vehículos de huéspedes y visitantes
- Edificios corporativos con tarifas diferenciadas por tipo de usuario
- Universidades con reservas para estudiantes y profesores

---

## Características

### Panel de Administración

- **Dashboard interactivo** con estadísticas en tiempo real
- **Gráficos dinámicos** de ingresos (últimos 7 días) y tendencias de ocupación por hora (Chart.js)
- **Vista general de pisos** con mapa visual de ocupación por espacio (orden estable en PostgreSQL)
- **Gestión de pisos, tipos de espacio y espacios** — creación individual o por rango
- **Inventario de parqueo** con historial completo de entradas/salidas
- **Registro de entrada/salida** con modal interactivo y cálculo automático de tarifas
- **Reportes** exportables en PDF estilizado (ReportLab) y Excel (openpyxl)
- **Gestión de usuarios** con roles, activación/desactivación y eliminación protegida por teclado
- **Cupones de descuento** con validación de uso único por usuario

### Panel Guardia (Vigilante)

- Dashboard exclusivo para el rol VIGILANTE
- Registrar ingreso de vehículos (busca por placa, asigna espacio disponible)
- Registrar salida con cálculo automático de cobro
- Confirmar pago en efectivo al momento de salida
- Vista de ocupación en tiempo real con indicadores de pagos pendientes

### Panel Cliente

- Dashboard personal con vehículos, reservas activas y stickers acumulados
- Gestión de vehículos propios (crear, editar)
- Reservas de espacios (crear, editar, cancelar, confirmar)
- Perfil con historial de stickers y bono de fidelidad
- Salida del parqueadero con pago en línea o generación de recibo para caja

### Recibos de Pago

- Generación de recibos imprimibles para **admin, vigilante y cliente**
- Control de acceso por rol: el cliente solo ve sus propios recibos
- Diseño con tema oscuro MultiParking, optimizado para impresión (`@media print`)
- Detalle de vehículo, duración, descuentos aplicados y monto final

### Sistema de Pagos y Tarifas

- **Tarifas flexibles** por hora, día o mes según tipo de espacio
- **Precio diferenciado para visitantes** (`precioHoraVisitante`)
- Cálculo automático: minutos/60 × precioHora, redondeado a 100 COP
- Solo una tarifa activa por tipo de espacio a la vez
- Estados de pago: Pagado / Pendiente (efectivo) / Anulado
- **Cupones** (porcentaje o valor fijo) con código único, uso único por usuario

### Sistema de Reservas

- Reserva de espacios por fecha y hora
- Estados: Pendiente → Confirmada → Completada / Cancelada
- Gestión desde panel admin y desde panel cliente
- Liberación automática de espacio al cancelar o completar

### Novedades (Incidentes)

- Registro de incidentes por vehículo y/o espacio
- Estados: PENDIENTE → EN_PROCESO → RESUELTO
- Soporte para fotos adjuntas (`ImageField`)
- Asignación de reportador y responsable, seguimiento con comentarios
- Notificación por email al registrar una novedad (SendGrid)

### Programa de Fidelidad

- Un sticker por cada parqueo de más de 1 hora (usuarios registrados)
- Meta configurable de stickers para canjear bono
- Al alcanzar la meta: cupón de 100% de descuento con vigencia configurable
- Panel de progreso en perfil del cliente

### Código QR

- Generación de QR por espacio para entrada rápida desde celular
- Escáner QR para registrar ingreso sin necesidad del guardia

### Páginas de Error Personalizadas

- **404** — página oscura con animación flotante y botón de regreso
- **500** — terminal animado, muestra cuando la base de datos no responde
- **403** — candado con animación, redirige al login
- Middleware `DatabaseErrorMiddleware` captura `OperationalError` antes de llegar al usuario

### Seguridad

- **Autenticación personalizada** — `Usuario` propio, sin `django.contrib.auth.User`
- Hashing de contraseñas con PBKDF2 (Django hashers)
- Recuperación de contraseña con token por email (SendGrid)
- **Roles**: ADMIN · VIGILANTE · CLIENTE con mixins de acceso (`AdminRequiredMixin`, etc.)
- `SecurityHeadersMiddleware`: `Content-Security-Policy` + `X-XSS-Protection`
- `NoCacheAfterLogoutMiddleware`: previene back-button tras cerrar sesión
- CSRF en todos los formularios
- Protección contra SQL injection vía ORM de Django

---

## Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.12+ |
| **Framework web** | Django 5.x |
| **Base de datos** | MySQL 8.0 (desarrollo) · PostgreSQL (producción — Render.com) |
| **Frontend** | Tailwind CSS (CDN) + Django Templates (SSR) |
| **Gráficos** | Chart.js (línea e histograma) |
| **Reportes** | ReportLab (PDF) · openpyxl (Excel) |
| **Email** | SendGrid (`django-sendgrid-v5`) |
| **Autenticación** | Sesiones personalizadas (sin `django.contrib.auth`) |
| **API** | Django REST Framework |
| **Servidor** | Gunicorn + WhiteNoise (archivos estáticos) |
| **Despliegue** | Render.com |

---

## Patrón de Diseño

El proyecto aplica el patrón **MVT (Model–View–Template)** de Django:

- **Model**: define la estructura de datos con validaciones y reglas de negocio (`validators`, `@property` calculados)
- **View**: Class-Based Views con mixins de autorización por rol; maneja lógica de negocio sin Django Forms
- **Template**: Server-Side Rendering con Tailwind CSS; AJAX puntual para operaciones sin recarga

Adicionalmente:
- **Middleware chain** para seguridad (CSP, no-cache, errores de BD)
- **Separación de responsabilidades** por app: cada módulo de negocio es una app Django independiente
- **Singleton pattern** en `ConfiguracionFidelidad` (pk=1 fijo)

---

## Arquitectura de Apps

```
multiparking/          ← Configuración, URLs, middleware, error views
usuarios/              ← Autenticación y gestión de usuarios
vehiculos/             ← Vehículos de usuarios registrados y visitantes
parqueadero/           ← Pisos, espacios, inventario, QR, reportes
tarifas/               ← Tarifas por tipo de espacio
pagos/                 ← Registro de pagos y recibos
cupones/               ← Cupones de descuento con validación de uso
reservas/              ← Reservas de espacios
novedades/             ← Incidentes y novedades operativas
fidelidad/             ← Programa de stickers y bonos
```

---

## Instalación

### Prerrequisitos

- Python 3.12+
- MySQL 8.0+
- Git

### Pasos

```bash
# 1. Clonar
git clone https://github.com/xeodeo/Multiparking-Django.git
cd Multiparking-Django

# 2. Entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Dependencias
pip install -r requirements.txt

# 4. Variables de entorno — copiar y editar
cp .env.example .env
```

`.env` mínimo para desarrollo:

```env
DB_NAME=multiparking_db
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=clave-secreta-larga
DEBUG=True
SENDGRID_API_KEY=opcional-en-dev
```

```bash
# 5. Base de datos
python manage.py migrate

# 6. Datos de demostración
python scripts/reiniciar_base_datos.py

# 7. Iniciar
python manage.py runserver
```

### URLs de acceso

| Panel | URL |
|-------|-----|
| Página pública | `http://127.0.0.1:8000/` |
| Admin | `http://127.0.0.1:8000/admin-panel/` |
| Guardia | `http://127.0.0.1:8000/guardia/` |
| Cliente | `http://127.0.0.1:8000/dashboard/` |

---

## Demo en Vivo

**[https://multiparking-django.onrender.com](https://multiparking-django.onrender.com)**

> Plan gratuito de Render — puede tardar 30–50 segundos en despertar (cold start).

### Credenciales de Prueba

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Administrador | `admin@multiparking.com` | `admin123` |
| Vigilante | `vigilante@multiparking.com` | `vigil123` |
| Cliente (Carlos) | `cliente@test.com` | `test123` |
| Cliente (María) | `maria@test.com` | `test123` |

### Cupones Activos

| Código | Descuento |
|--------|-----------|
| `BIENVENIDO20` | 20% |
| `DESCUENTO5K` | $5.000 fijo |
| `FINDE50` | 50% |
| `VIPPREMIUM` | 30% |

---

## Estructura del Proyecto

```
Multiparking-Django/
├── multiparking/
│   ├── settings.py          # Config MySQL/PostgreSQL, timezone Bogotá
│   ├── urls.py              # URLs completas (admin, guardia, cliente, API)
│   ├── middleware.py        # DatabaseError, SecurityHeaders, NoCache
│   └── error_views.py       # Handlers 404 / 500 / 403
│
├── usuarios/                # Auth personalizada
├── vehiculos/               # CRUD vehículos (admin + cliente)
├── parqueadero/             # Core: pisos, espacios, inventario, QR, reportes
├── tarifas/                 # Tarifas por tipo de espacio
├── pagos/                   # Pagos + recibos imprimibles
├── cupones/                 # Cupones con uso único por usuario
├── reservas/                # Reservas (admin + cliente)
├── novedades/               # Incidentes con foto y seguimiento
├── fidelidad/               # Stickers y bonos de fidelidad
│
├── templates/
│   ├── 404.html / 500.html / 403.html   # Páginas de error
│   ├── recibo/recibo.html               # Recibo imprimible
│   ├── admin_panel/                     # Panel administrador
│   ├── vigilante/                       # Panel guardia
│   └── cliente/                         # Panel cliente
│
├── scripts/
│   ├── reiniciar_base_datos.py          # Reset + seed completo
│   ├── render_datos_prueba.py           # Seed para producción (PostgreSQL)
│   └── DATOS_DEMO.md                    # Guía de scripts
│
├── requirements.txt
├── .env.example
└── build.sh                             # Script de despliegue en Render
```

---

## Convenciones del Código

- **Campos de modelos**: camelCase con prefijo de tabla (`usuNombre`, `vehPlaca`, `espEstado`, `parHoraEntrada`)
- **Foreign Keys**: `fkId<Entidad>` con `db_column` explícito
- **Tablas**: nombres en minúsculas (`usuarios`, `vehiculos`, `espacios`, `inventario_parqueo`)
- **Vistas**: Class-Based Views sin Django Forms — validación directa sobre `request.POST`
- **Idioma**: Español para dominio de negocio, inglés para términos técnicos/framework
- **Timezone**: `America/Bogota` (UTC-5) · **Locale**: `es-co`

---

## Seguridad

| Mecanismo | Implementación |
|-----------|---------------|
| Hashing contraseñas | PBKDF2 con Django hashers |
| Control de acceso | Mixins por rol: Admin / Vigilante / Cliente |
| Headers HTTP | CSP restringida + X-XSS-Protection |
| Caché tras logout | `Cache-Control: no-store` en sesiones activas |
| CSRF | Token en todos los formularios |
| SQL Injection | Protección automática ORM |
| Errores de BD | `DatabaseErrorMiddleware` → página 500 estática |
| Password reset | Token único por email (SendGrid) |

---

## Roadmap

### ✅ Completado
- Panel administrador, guardia y cliente completos
- Novedades e incidentes con fotos
- Programa de fidelidad con stickers y bonos
- Código QR para entrada rápida
- Reportes PDF y Excel con diseño
- Recibos imprimibles por rol
- Recuperación de contraseña
- Tarifas diferenciadas (registrado vs visitante)
- Páginas de error 404 / 500 / 403 personalizadas
- Middleware de error de base de datos

### 🔜 Próximas Funcionalidades
- Notificaciones push / SMS al registrar entrada/salida
- Pagos en línea (PSE, PayU, Stripe)
- Reconocimiento de placas con OCR
- API REST completa con documentación Swagger
- Multi-tenant (soporte para múltiples parqueaderos)

---

## Licencia

MIT License.

---

<div align="center">
Desarrollado con dedicación por el equipo de <strong>MultiParking</strong> — Colombia 🇨🇴
</div>
