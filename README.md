# MultiParking

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0_dev-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-producción-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CDN-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Sistema de gestión inteligente para parqueaderos multinivel**

[Demo en Vivo](https://multiparking-django.onrender.com) | [Instalación](#-instalación) | [Características](#-características)

</div>

---

## Descripción

**MultiParking** es una aplicación web desarrollada en Django para la administración completa de parqueaderos de múltiples pisos. Permite gestionar usuarios, vehículos, espacios de parqueo, reservas, tarifas dinámicas, pagos, cupones de descuento, novedades (incidentes) y un programa de fidelidad con stickers.

### Casos de Uso

- Centros comerciales con parqueadero multinivel
- Hoteles con gestión de vehículos de huéspedes
- Edificios corporativos con control de acceso vehicular
- Universidades con reservas para estudiantes y profesores
- Hospitales con gestión de parqueo para pacientes y personal

---

## Características

### Panel de Administración

- **Dashboard interactivo** con estadísticas en tiempo real
- **Gráficos dinámicos** de ingresos (últimos 7 días) y tendencias de ocupación por hora (Chart.js)
- **Gestión de pisos** con visualización de capacidad y porcentaje de ocupación
- **Tipos de espacios** configurables (Carro, Moto, etc.)
- **Inventario de parqueo** con historial completo de entradas/salidas
- **Registro de entrada/salida** con modal interactivo y cálculo automático de tarifas
- **Reportes** exportables en PDF (reportlab) y Excel (openpyxl)
- **Gestión de usuarios** con roles y activación/desactivación

### Panel Guardia (Vigilante)

- Dashboard exclusivo para el rol VIGILANTE
- Registrar ingreso de vehículos (busca por placa, asigna espacio)
- Registrar salida y confirmar pago
- Vista de ocupación en tiempo real

### Panel Cliente

- Dashboard personal con vehículos, reservas y stickers
- Gestión de vehículos propios (crear, editar)
- Reservas de espacios (crear, editar, cancelar, confirmar)
- Perfil con historial de stickers y bono de fidelidad
- Salida del parqueadero mediante QR

### Gestión de Vehículos

- Registro de vehículos de **usuarios registrados** y **visitantes**
- Búsqueda rápida por placa
- Información de contacto para visitantes (nombre y teléfono)
- Historial de parqueos por vehículo

### Sistema de Pagos y Tarifas

- **Tarifas flexibles** por hora, día o mes según tipo de espacio
- **Precio diferenciado para visitantes** (`precioHoraVisitante`)
- Cálculo automático del monto según tiempo de estadía (redondeo hacia arriba a 100 COP)
- Solo una tarifa activa por tipo de espacio a la vez
- Registro de pagos con estados (Pagado/Pendiente)
- **Cupones de descuento** (porcentaje o valor fijo) con código único

### Sistema de Reservas

- Reserva de espacios por fecha y hora
- Estados: Pendiente, Confirmada, Completada, Cancelada
- Gestión desde panel admin y desde panel cliente
- Liberación automática de espacios al cancelar/completar

### Novedades (Incidentes)

- Registro de incidentes por vehículo y/o espacio
- Estados: PENDIENTE, EN_PROCESO, RESUELTO
- Soporte para fotos adjuntas
- Asignación de responsable y seguimiento con comentarios

### Programa de Fidelidad (Stickers)

- Un sticker por cada parqueo de más de 1 hora (usuarios registrados)
- Meta configurable de stickers para canjear bono
- Al alcanzar la meta: cupón de 100% de descuento con vigencia configurable
- Panel de progreso en perfil del cliente

### Código QR

- Generación de QR por espacio para entrada rápida
- Escáner QR para registrar ingreso desde el celular del cliente

### Interfaz Moderna

- **Diseño Dark Mode** con paleta de colores personalizada (mp-dark, mp-purple)
- **Tailwind CSS** para diseño responsivo y moderno
- Barra de reloj en tiempo real con fecha y hora en español
- Date pickers con tema oscuro personalizado
- Estados visuales con badges de colores (Disponible, Ocupado, Reservado, Inactivo)

### Seguridad

- **Sistema de autenticación personalizado** (sin django.contrib.auth)
- Hashing de contraseñas con PBKDF2 (Django hashers)
- **Recuperación de contraseña** via email (SendGrid)
- **Control de acceso basado en roles**: Admin, Vigilante, Cliente
- **CSP + X-XSS-Protection** vía `SecurityHeadersMiddleware`
- **No-cache tras logout** vía `NoCacheAfterLogoutMiddleware`
- Protección CSRF en todos los formularios

---

## Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| **Backend** | Django 6.0, Python 3.12+ |
| **Base de Datos** | MySQL 8.0 (dev) · PostgreSQL (producción en Render) |
| **Frontend** | Tailwind CSS (CDN) + Django Templates |
| **Gráficos** | Chart.js (Line & Bar) |
| **Reportes** | reportlab (PDF), openpyxl (Excel) |
| **Email** | SendGrid (`django-sendgrid-v5`) |
| **Autenticación** | Sesiones personalizadas (sin django.contrib.auth.User) |
| **APIs** | Django REST Framework |
| **Despliegue** | Render.com + Gunicorn + WhiteNoise |

---

## Instalación

### Prerrequisitos

- Python 3.12 o superior
- MySQL 8.0 o superior
- pip
- Git

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/multiparking.git
cd multiparking
```

2. **Crear entorno virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos MySQL (desarrollo)
DB_NAME=multiparking_db
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=tu_secret_key_super_segura_aqui
DEBUG=True

# Email (opcional en dev)
SENDGRID_API_KEY=tu_api_key
DEFAULT_FROM_EMAIL=noreply@multiparking.com
```

5. **Crear base de datos MySQL**

```sql
CREATE DATABASE multiparking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **Ejecutar migraciones**

```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Cargar datos de prueba**

```bash
# Opción A: solo usuario admin
python create_admin.py

# Opción B: base de datos completa con datos demo
python scripts/reiniciar_base_datos.py
```

8. **Iniciar servidor**

```bash
python manage.py runserver
```

9. **Acceder**

- Página pública: `http://127.0.0.1:8000`
- Panel admin: `http://127.0.0.1:8000/admin-panel/`
- Panel guardia: `http://127.0.0.1:8000/guardia/`
- Dashboard cliente: `http://127.0.0.1:8000/dashboard/`

---

## Estructura del Proyecto

```
multiparking/
├── multiparking/              # Configuración principal del proyecto
│   ├── settings.py            # MySQL dev / PostgreSQL prod, timezone Bogotá
│   ├── urls.py                # URLs principales (admin, guardia, cliente, API)
│   ├── middleware.py          # SecurityHeadersMiddleware, NoCacheAfterLogoutMiddleware
│   └── wsgi.py
│
├── usuarios/                  # Autenticación personalizada
│   ├── models.py              # Usuario (custom, sin django.contrib.auth)
│   ├── views.py               # Login, Register, Logout, Password Reset, CRUD admin
│   └── mixins.py              # AdminRequiredMixin, VigilanteRequiredMixin
│
├── parqueadero/               # App principal - Gestión del parqueadero
│   ├── models.py              # Piso, TipoEspacio, Espacio, InventarioParqueo
│   ├── views.py               # CRUD admin + Dashboard + Entrada/Salida + QR
│   ├── vigilante_views.py     # Vistas exclusivas del panel guardia
│   ├── cliente_views.py       # Salida del parqueadero para cliente
│   └── reportes_views.py      # Exportar PDF y Excel
│
├── vehiculos/                 # Gestión de vehículos
│   ├── models.py              # Vehiculo (usuarios registrados y visitantes)
│   ├── views.py               # CRUD admin
│   └── cliente_views.py       # CRUD para el cliente
│
├── tarifas/                   # Sistema de tarifas
│   ├── models.py              # Tarifa (precioHora, precioHoraVisitante, precioDia, precioMensual)
│   └── views.py               # CRUD + toggle activa
│
├── pagos/                     # Registro de pagos
│   ├── models.py              # Pago
│   └── views.py               # Lista de pagos
│
├── cupones/                   # Sistema de cupones
│   ├── models.py              # Cupon (con cupCodigo), CuponAplicado
│   └── views.py               # CRUD de cupones
│
├── reservas/                  # Sistema de reservas
│   ├── models.py              # Reserva
│   ├── views.py               # CRUD admin + Finalizar/Cancelar
│   └── cliente_views.py       # Crear/editar/cancelar para cliente
│
├── novedades/                 # Incidentes y novedades
│   ├── models.py              # Novedad (descripción, foto, estado, comentario)
│   └── views.py               # CRUD de novedades
│
├── fidelidad/                 # Programa de fidelidad
│   ├── models.py              # ConfiguracionFidelidad (singleton), Sticker
│   └── views.py               # Config admin + Perfil cliente + Reclamar bono
│
├── templates/
│   ├── base.html              # Template base público
│   ├── home.html              # Página de inicio
│   ├── auth/                  # Login, Register, Password Reset, Dashboard cliente
│   ├── vigilante/             # Panel del guardia
│   ├── cliente/               # Perfil, vehículos, reservas del cliente
│   └── admin_panel/           # Panel administrativo completo
│       ├── base.html          # Layout admin (sidebar + header + reloj)
│       ├── dashboard.html
│       ├── pisos/, espacios/, vehiculos/
│       ├── tarifas/, cupones/, reservas/
│       ├── inventario/, pagos/, reportes/
│       ├── novedades/, fidelidad/
│       └── usuarios/
│
├── scripts/
│   ├── reiniciar_base_datos.py   # Reset + seed completo (dev)
│   ├── render_datos_prueba.py    # Seed para Render (prod)
│   ├── cargar_datos_iniciales.py # Solo estructura base
│   ├── mantener_datos_demo.py    # Mantener pagos demo actualizados
│   └── DATOS_DEMO.md             # Guía de scripts de datos
│
├── create_admin.py            # Crea usuario admin rápidamente
├── requirements.txt
├── .env.example
└── README.md
```

---

## Uso del Sistema

### Como Administrador

1. Iniciar sesión en `/login/` con credenciales de admin
2. **Configurar el parqueadero:** pisos → tipos de espacio → espacios (individual o por rango)
3. **Configurar tarifas** por tipo de espacio con precios diferenciados (usuario / visitante)
4. **Registrar novedades** de incidentes por vehículo o espacio
5. **Ver reportes** y exportarlos en PDF o Excel
6. **Gestionar fidelidad:** configurar meta de stickers y vigencia del bono

### Como Vigilante (Guardia)

1. Iniciar sesión → redirige automáticamente a `/guardia/`
2. **Registrar ingreso**: buscar vehículo por placa → asignar espacio → confirmar
3. **Registrar salida**: seleccionar vehículo → calcular cobro → confirmar pago
4. Ver ocupación en tiempo real del parqueadero

### Como Cliente

1. Registrarse en `/register/`
2. **Dashboard** (`/dashboard/`): resumen de vehículos, reservas activas y stickers
3. **Reservar** un espacio con fecha y hora
4. **Perfil** (`/cliente/perfil/`): ver stickers acumulados y reclamar bono
5. **Salida QR**: escanear código del espacio al salir

---

## Demo en Vivo

**[https://multiparking-django.onrender.com](https://multiparking-django.onrender.com)**

> La aplicación está en el plan gratuito de Render — puede tardar 30-50 segundos en despertar (cold start).

### Credenciales de Prueba

| Rol | Email | Password |
|-----|-------|----------|
| Administrador | `admin@multiparking.com` | `admin123` |
| Vigilante | `vigilante@multiparking.com` | `vigil123` |
| Cliente 1 (Carlos Perez) | `cliente@test.com` | `test123` |
| Cliente 2 (Maria Lopez) | `maria@test.com` | `test123` |

### Cupones de Descuento

| Código | Descuento |
|--------|-----------|
| `BIENVENIDO20` | 20% |
| `DESCUENTO5K` | $5,000 fijo |
| `FINDE50` | 50% |
| `VIPPREMIUM` | 30% |

---

## Convenciones del Código

### Nomenclatura de Modelos

- **Campos**: camelCase con prefijo de tabla
  - Usuario: `usuDocumento`, `usuNombre`, `usuApellido`, `usuCorreo`, `usuClaveHash`
  - Vehículo: `vehPlaca`, `vehTipo`, `vehMarca`
  - Espacio: `espNumero`, `espEstado`
  - Inventario: `parHoraEntrada`, `parHoraSalida`
  - Novedad: `novDescripcion`, `novEstado`, `novComentario`
  - Sticker: `stkFecha`

- **Foreign Keys**: `fkId<Entity>` con `db_column` explícito
  - `fkIdPiso`, `fkIdVehiculo`, `fkIdEspacio`, `fkIdTipoEspacio`, `fkIdReportador`

- **Tablas**: nombres en minúsculas
  - `usuarios`, `vehiculos`, `espacios`, `inventario_parqueo`, `novedades`, `fidelidad_stickers`

### Arquitectura

- **Vistas**: Class-based views (CBV) con patrón CRUD
- **Templates**: Server-side rendering con Django Template Language
- **Sin Django Forms**: validación manual en vistas (mayor control)
- **Idioma mixto**: Español para dominio de negocio, inglés para términos técnicos
- **Timezone**: `America/Bogota` (UTC-5)
- **Locale**: `es-co` (español Colombia)

---

## Seguridad

- **Hashing**: PBKDF2 con Django hashers
- **Roles**: `ADMIN` (panel completo), `VIGILANTE` (operaciones de parqueo), `CLIENTE` (self-service)
- **CSP**: `Content-Security-Policy` restringida a self + Tailwind CDN
- **No-cache**: headers para prevenir back-button tras logout
- **CSRF**: tokens en todos los formularios
- **SQL Injection**: protección automática con ORM de Django
- **Recuperación de contraseña**: tokens únicos por email vía SendGrid

---

## Roadmap

### Completado
- [x] Panel de administración completo
- [x] Panel vigilante/guardia dedicado
- [x] Panel cliente con self-service
- [x] Novedades e incidentes
- [x] Programa de fidelidad con stickers
- [x] Código QR para entrada
- [x] Reportes PDF y Excel
- [x] Recuperación de contraseña
- [x] Tarifas diferenciadas (usuario vs visitante)

### Próximas Funcionalidades
- [ ] Notificaciones push / SMS al registrar entrada/salida
- [ ] Pagos en línea (PSE, PayU, Stripe)
- [ ] Reconocimiento de placas con OCR
- [ ] API REST completa con Swagger
- [ ] Multi-tenant (soporte para múltiples parqueaderos)

---

## Licencia

MIT License. Ver `LICENSE` para más detalles.

---

<div align="center">

Desarrollado con dedicación por el equipo de **MultiParking** — Colombia

</div>
