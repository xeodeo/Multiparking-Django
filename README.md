# 🚗 MultiParking

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Sistema de gestión inteligente para parqueaderos multinivel**

[🌐 Demo en Vivo](https://multiparking-django.onrender.com) | [📖 Documentación](#-características) | [🚀 Instalación](#-instalación)

</div>

---

## 📋 Descripción

**MultiParking** es una aplicación web desarrollada en Django para la administración completa de parqueaderos de múltiples pisos. Permite gestionar usuarios, vehículos, espacios de parqueo, reservas, tarifas dinámicas, pagos y cupones de descuento con una interfaz moderna y responsiva.

### 🎯 Casos de Uso

- 🏢 **Centros comerciales** con parqueadero multinivel
- 🏨 **Hoteles** con gestión de vehículos de huéspedes
- 🏛️ **Edificios corporativos** con control de acceso vehicular
- 🎓 **Universidades** con reservas para estudiantes y profesores
- 🏥 **Hospitales** con gestión de parqueo para pacientes y personal

---

## ✨ Características

### 🎛️ Panel de Administración

- **Dashboard interactivo** con estadísticas en tiempo real
- **Gráficos dinámicos** de ingresos (últimos 7 días) y tendencias de ocupación por hora (Chart.js)
- **Gestión de pisos** con visualización de capacidad y porcentaje de ocupación
- **Tipos de espacios** configurables (Estándar, VIP, Moto, Discapacitados, etc.)
- **Inventario de parqueo** con historial completo de entradas/salidas
- **Registro de entrada/salida** con modal interactivo y cálculo automático de tarifas

### 🚘 Gestión de Vehículos

- Registro de vehículos de **usuarios registrados** y **visitantes**
- Búsqueda rápida por placa
- Información de contacto para visitantes (nombre y teléfono)
- Historial de parqueos por vehículo
- Tipos de vehículos: Carro, Moto, Camioneta, etc.

### 💰 Sistema de Pagos y Tarifas

- **Tarifas flexibles** por hora, día o mes según tipo de espacio
- Cálculo automático del monto según tiempo de estadía (redondeo hacia arriba)
- Solo una tarifa activa por tipo de espacio a la vez
- Registro de pagos con estados (Pagado/Pendiente)
- **Cupones de descuento** (porcentaje o valor fijo)
- Validación de cupones por fecha de vigencia (desde/hasta)

### 📅 Sistema de Reservas

- Reserva de espacios por fecha y hora
- Estados: Pendiente, Confirmada, Completada, Cancelada
- Búsqueda y filtrado de reservas por placa, espacio o estado
- Finalización y cancelación con liberación automática de espacios
- Vista previa de reservas activas en el dashboard

### 🎨 Interfaz Moderna

- **Diseño Dark Mode** con paleta de colores personalizada (mp-dark, mp-purple)
- Componentes estilo **iPhone toggle** para checkboxes (Tailwind peer classes)
- **Tailwind CSS** para diseño responsivo y moderno
- Animaciones fluidas y transiciones suaves
- Barra de reloj en tiempo real con fecha y hora en español
- Date pickers con tema oscuro personalizado
- Estados visuales con badges de colores (🟢 Disponible, 🔴 Ocupado, 🟡 En curso, etc.)

### 🔐 Seguridad y Autenticación

- **Sistema de autenticación personalizado** (sin django.contrib.auth)
- Hashing de contraseñas con Django hashers (PBKDF2)
- **Control de acceso basado en roles**: Admin, Vigilante, Cliente
- Validación de duplicados (documento y correo único)
- Mixins de autorización para vistas protegidas (`AdminRequiredMixin`)
- CSRF protection en todos los formularios
- Gestión de sesiones segura

---

## 🛠️ Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| **Backend** | ![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django) Python 3.10+ |
| **Base de Datos** | ![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white) (utf8mb4) |
| **Frontend** | ![TailwindCSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC?logo=tailwind-css&logoColor=white) + Django Templates |
| **Gráficos** | Chart.js (Line & Bar charts) |
| **Autenticación** | Sistema de sesiones personalizado |
| **APIs** | Django REST Framework (DRF) |
| **Servidor de Desarrollo** | Django Dev Server |
| **Despliegue** | ![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?logo=render&logoColor=white) + Gunicorn + WhiteNoise |

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)
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

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crear archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Base de datos MySQL
DB_NAME=multiparking_db
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=tu_secret_key_super_segura_aqui
DEBUG=True

# Configuración adicional
ALLOWED_HOSTS=localhost,127.0.0.1
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

7. **Crear usuario administrador**

```bash
python create_admin.py
```

Esto creará un usuario administrador con las siguientes credenciales:
- **Email:** `admin@multiparking.com`
- **Password:** `admin123`

8. **Iniciar servidor de desarrollo**

```bash
python manage.py runserver
```

9. **Acceder a la aplicación**

- **Frontend público:** `http://127.0.0.1:8000`
- **Panel de administración:** `http://127.0.0.1:8000/admin-panel/`

---

## 📱 Estructura del Proyecto

```
multiparking/
├── multiparking/              # Configuración principal del proyecto
│   ├── settings.py            # Configuración (MySQL, timezone Bogotá, locale es-co)
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # WSGI para despliegue
│
├── parqueadero/               # App principal - Gestión de parqueadero
│   ├── models.py              # Piso, TipoEspacio, Espacio, InventarioParqueo
│   ├── views.py               # Vistas CRUD + Dashboard + Operaciones
│   └── urls.py                # URLs de parqueadero
│
├── usuarios/                  # Autenticación personalizada
│   ├── models.py              # Usuario (custom user model)
│   ├── views.py               # Login, Register, Logout
│   └── mixins.py              # AdminRequiredMixin
│
├── vehiculos/                 # Gestión de vehículos
│   ├── models.py              # Vehiculo (usuarios y visitantes)
│   └── views.py               # CRUD de vehículos
│
├── tarifas/                   # Sistema de tarifas
│   ├── models.py              # Tarifa (precioHora, precioDia, precioMensual)
│   └── views.py               # CRUD de tarifas + toggle activa
│
├── pagos/                     # Registro de pagos
│   ├── models.py              # Pago (monto, método, estado)
│   └── views.py               # Vistas de pagos
│
├── cupones/                   # Sistema de cupones de descuento
│   ├── models.py              # Cupon, CuponAplicado
│   └── views.py               # CRUD de cupones
│
├── reservas/                  # Sistema de reservas
│   ├── models.py              # Reserva (fecha, hora, estado)
│   └── views.py               # CRUD + Finalizar/Cancelar
│
├── templates/
│   ├── base.html              # Template base público
│   ├── home.html              # Página de inicio
│   ├── auth/                  # Login, Register, Dashboard cliente
│   └── admin_panel/           # Plantillas del panel admin
│       ├── base.html          # Layout admin (sidebar + header + reloj)
│       ├── dashboard.html     # Dashboard principal
│       ├── pisos/             # CRUD Pisos
│       ├── espacios/          # CRUD Espacios
│       ├── vehiculos/         # CRUD Vehículos
│       ├── tarifas/           # CRUD Tarifas
│       ├── cupones/           # CRUD Cupones
│       ├── reservas/          # Lista + Acciones
│       └── inventario/        # Historial de entradas/salidas
│
├── create_admin.py            # Script para crear usuario admin
├── requirements.txt           # Dependencias Python
├── .env.example               # Ejemplo de variables de entorno
└── README.md                  # Este archivo
```

---

## 🎯 Uso del Sistema

### 1️⃣ Como Administrador

1. **Iniciar sesión** en `/login/` con credenciales de admin
2. **Configurar el parqueadero:**
   - Crear pisos (ej: Piso 1, Piso 2, Sótano)
   - Definir tipos de espacios (Estándar, VIP, Moto, Discapacitados)
   - Generar espacios (individual o por rango: A-001 a A-050)
3. **Configurar tarifas:**
   - Crear tarifas por tipo de espacio
   - Definir precios por hora/día/mes
   - Activar/desactivar tarifas
4. **Registrar vehículos:**
   - Usuarios registrados (vinculados a cuentas)
   - Visitantes (datos de contacto temporales)
5. **Operaciones diarias:**
   - Registrar entrada: seleccionar vehículo → asignar espacio → confirmar
   - Registrar salida: desde Dashboard o Inventario → cálculo automático → pago
6. **Gestión de reservas:**
   - Ver reservas activas en dashboard
   - Finalizar o cancelar reservas desde `/admin-panel/reservas/`
7. **Análisis:**
   - Ver gráficos de ingresos (últimos 7 días)
   - Ver tendencias de ocupación por hora
   - Consultar inventario completo con búsqueda

### 2️⃣ Como Cliente (Usuario Registrado)

1. **Registrarse** en `/register/` con documento, nombre, correo y contraseña
2. **Iniciar sesión** en `/login/`
3. **Acceder al dashboard** cliente en `/dashboard/`
4. Ver historial de parqueos (próximamente)
5. Realizar reservas (próximamente)

---

## 🌟 Capturas de Pantalla

<details>
<summary><b>🖼️ Ver capturas</b></summary>

### 🏠 Página de Inicio
Interfaz de bienvenida con opciones de login y registro.

### 📊 Dashboard Administrativo
Panel principal con:
- Stats cards: Total espacios, Disponibles, Ocupados, Reservas activas
- Gráfico de ingresos últimos 7 días (Chart.js line)
- Gráfico de ocupación por hora del día (Chart.js bar)
- Tabla de reservas recientes
- Vista de pisos con porcentaje de ocupación

### 📦 Inventario de Parqueo
Historial completo de entradas y salidas:
- Cards con stats: Vehículos Dentro, Salidas Hoy, Total Registros
- Búsqueda por placa o espacio
- Tabla con estados visuales (🟡 En curso, 🟢 Finalizado)
- Botón "Registrar Salida" para entradas activas

### 🚗 Gestión de Espacios
Lista de espacios por piso con:
- Filtros por piso y estado
- Badges de estado (Disponible/Ocupado/Inactivo)
- Acciones: Editar, Eliminar
- Creación individual o por rango

### 💵 Sistema de Tarifas
Configuración de precios:
- Tarifa por hora, día y mes
- Toggle iPhone-style para activar/desactivar
- Solo una activa por tipo de espacio
- Date pickers oscuros personalizados

### 🎫 Cupones de Descuento
Gestión de cupones:
- Descuento por porcentaje o valor fijo
- Fechas de vigencia (desde/hasta)
- Estados activo/inactivo con toggle
- Validación automática de fechas

</details>

---

## 🔐 Seguridad

- **Hashing de contraseñas**: PBKDF2 con Django hashers
- **Validación de duplicados**: Documento y correo únicos en registro
- **Control de acceso por roles**:
  - `ADMIN`: Acceso completo al panel administrativo
  - `VIGILANTE`: Operaciones de entrada/salida
  - `CLIENTE`: Dashboard personal y reservas
- **Protección CSRF**: Tokens en todos los formularios
- **Sesiones seguras**: Validación en cada request
- **Mixins de autorización**: `AdminRequiredMixin` protege vistas admin
- **SQL Injection**: Protección automática con ORM de Django

---

## 🌍 Demo en Vivo

🚀 **Accede a la aplicación desplegada:**

### **[https://multiparking-django.onrender.com](https://multiparking-django.onrender.com)**

### Credenciales de Prueba:

**👤 Administrador:**
- **Email:** `admin@multiparking.com`
- **Password:** `admin123`

**🎯 Funcionalidades disponibles en la demo:**
- ✅ Panel de administración completo
- ✅ Gestión de pisos, espacios, vehículos
- ✅ Registro de entradas y salidas
- ✅ Tarifas y cupones
- ✅ Sistema de reservas
- ✅ Inventario y reportes

> **⚠️ Nota Importante:** La aplicación está desplegada en el plan gratuito de Render. Si no ha sido usada recientemente, puede tardar aproximadamente 30-50 segundos en "despertar" (cold start). Ten paciencia en la primera carga.

---

## 📝 Convenciones del Código

### Nomenclatura de Modelos

- **Campos**: camelCase con prefijo de tabla
  - Usuario: `usuDocumento`, `usuNombreCompleto`, `usuCorreo`, `usuClaveHash`
  - Vehículo: `vehPlaca`, `vehTipo`, `vehMarca`
  - Espacio: `espNumero`, `espEstado`
  - Inventario: `parHoraEntrada`, `parHoraSalida`

- **Foreign Keys**: `fkId<Entity>` con `db_column` explícito
  - `fkIdPiso`, `fkIdVehiculo`, `fkIdEspacio`, `fkIdTipoEspacio`

- **Tablas**: nombres en minúsculas plural
  - `usuarios`, `vehiculos`, `espacios`, `inventario_parqueo`

### Arquitectura

- **Vistas**: Class-based views (CBV) con patrón CRUD
  - `<Entity>ListView`, `<Entity>CreateView`, `<Entity>UpdateView`, `<Entity>DeleteView`
- **Templates**: Server-side rendering con Django Template Language
- **Sin Django Forms**: Validación manual en vistas (más control)
- **Idioma mixto**: Español para dominio de negocio, inglés para términos técnicos
- **Timezone**: `America/Bogota` (UTC-5)
- **Locale**: `es-co` (español Colombia)

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Add: Nueva funcionalidad increíble'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

### Guía de estilo:
- Seguir convenciones de nomenclatura del proyecto
- Incluir docstrings en funciones complejas
- Probar cambios antes de hacer PR
- Mantener commits atómicos y descriptivos

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

Desarrollado con ❤️ por el equipo de **MultiParking**

---

## 📞 Soporte

¿Tienes preguntas, problemas o sugerencias?

- 🐛 Reporta bugs: Abre un [issue](https://github.com/tu-usuario/multiparking/issues)
- 💡 Solicita features: Usa el [issue tracker](https://github.com/tu-usuario/multiparking/issues)
- 📧 Contacto directo: [email protected]

---

## 🗺️ Roadmap

### 🚧 Próximas Funcionalidades

- [ ] **Dashboard para clientes**: Historial personal de parqueos
- [ ] **Sistema de notificaciones**: Email/SMS al registrar entrada/salida
- [ ] **Reportes avanzados**: Exportar a PDF/Excel
- [ ] **Aplicación móvil**: React Native o Flutter
- [ ] **Pagos en línea**: Integración con PSE, PayU, Stripe
- [ ] **Reconocimiento de placas**: OCR con cámaras
- [ ] **API REST completa**: Endpoints documentados con Swagger
- [ ] **Reservas automáticas**: Integración con Google Calendar
- [ ] **Multi-tenant**: Soporte para múltiples parqueaderos

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/multiparking?style=social)](https://github.com/tu-usuario/multiparking/stargazers)

---

**Hecho con** 🚗 **y** ☕ **en Colombia**

</div>
