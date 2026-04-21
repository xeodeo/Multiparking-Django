# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Multiparking** — a Django web application for managing a multi-floor parking lot. Handles users, vehicles, parking spaces, entry/exit tracking, reservations, tariffs, payments, discount coupons, incident reports, and a loyalty sticker program.

Language: Spanish for business-domain names, English for framework/technical terms.

## Development Commands

```bash
# Install dependencies (requires MySQL client libraries locally)
pip install -r requirements.txt

# Configure database — copy .env.example to .env and set MySQL credentials
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (admin@multiparking.com / admin123)
python create_admin.py

# Run development server
python manage.py runserver

# Reset + reseed full database (dev)
python scripts/reiniciar_base_datos.py

# Seed test data for Render deployment
python scripts/render_datos_prueba.py
```

## Architecture

### Django Project: `multiparking/`
Settings module. Uses MySQL locally (utf8mb4), PostgreSQL on Render.com via `dj-database-url`. Timezone `America/Bogota`, locale `es-co`. Env vars loaded via `python-dotenv`.

### Apps

| App | Responsibility |
|---|---|
| `usuarios` | Custom `Usuario` model (NOT Django's auth User), login/register/logout views, password reset via SendGrid, session management, `AdminRequiredMixin` |
| `vehiculos` | `Vehiculo` model — supports both registered users and visitors (`es_visitante` is a `@property`, not a DB column). Separate `cliente_views.py` for client-side CRUD. |
| `parqueadero` | Core parking logic: `Piso`, `TipoEspacio`, `Espacio`, `InventarioParqueo`. All admin panel CRUD views. Entry/exit operations, QR code scanning, reportes PDF/Excel. |
| `tarifas` | `Tarifa` model — pricing per hour/day/month linked to `TipoEspacio`. Includes `precioHoraVisitante` for unregistered visitors. |
| `pagos` | `Pago` model — payment records linked to `InventarioParqueo` |
| `cupones` | `Cupon` and `CuponAplicado` models — discount coupons (percentage or fixed value), identified by `cupCodigo` |
| `reservas` | `Reserva` model — space reservations by date/time. Separate `cliente_views.py` for client self-service. |
| `novedades` | `Novedad` model — incident/event reports tied to a vehicle and/or space. States: PENDIENTE, EN_PROCESO, RESUELTO. Supports photo upload. |
| `fidelidad` | `ConfiguracionFidelidad` (singleton) + `Sticker` model — loyalty program: one sticker per parking stay > 1 hour; reaching the configured target generates a 100% discount coupon. |

### Authentication & Authorization

- **Custom session-based auth** — does NOT use `django.contrib.auth` User model. The `Usuario` model stores `usuClaveHash` (hashed with `django.contrib.auth.hashers`).
- Session keys: `usuario_id`, `usuario_nombre`, `usuario_rol`, `usuario_correo`.
- Three roles via `rolTipoRol` ENUM: `ADMIN`, `VIGILANTE`, `CLIENTE`.
- Admin-only views use `AdminRequiredMixin` (in `usuarios/mixins.py`) which checks session role.
- Password reset: token-based flow via SendGrid email (`django-sendgrid-v5`).

### URL Structure

- `/` — public home, `/login/`, `/register/`, `/logout/`
- `/dashboard/` — client dashboard
- `/password-reset/` — password recovery flow
- `/admin-panel/` — admin dashboard and all CRUD views:
  - `/admin-panel/pisos/`, `/admin-panel/tipos-espacio/`, `/admin-panel/espacios/`
  - `/admin-panel/tarifas/`, `/admin-panel/cupones/`, `/admin-panel/vehiculos/`
  - `/admin-panel/reservas/`, `/admin-panel/inventario/`, `/admin-panel/pagos/`
  - `/admin-panel/novedades/`, `/admin-panel/fidelidad/`
  - `/admin-panel/usuarios/`, `/admin-panel/reportes/`
  - `/admin-panel/qr/generar/`
- `/guardia/` — vigilante (guard) panel: registrar-ingreso, registrar-salida, confirmar-pago
- `/parqueadero/` — QR scan entry (`/escanear/`), entrada, salida
- `/cliente/` — client self-service: vehiculos, reservas, perfil, reclamar-bono
- `/api/<app>/` — REST API endpoints (DRF installed, serializers not yet fully implemented)

### Frontend

- Server-side rendering with Django Templates + Tailwind CSS (via CDN).
- Templates in `templates/` root directory: `base.html`, `home.html`, `auth/`, `admin_panel/`, `vigilante/`, `cliente/`.
- `admin_panel/base.html` is the layout for all admin views; each view passes `active_page` for sidebar highlighting.
- AJAX calls use `X-Requested-With: XMLHttpRequest` header; views return `JsonResponse` for AJAX, rendered HTML otherwise.

### Security Middleware

Two custom middleware classes in `multiparking/middleware.py`:

- **`SecurityHeadersMiddleware`**: Adds `Content-Security-Policy` (restricts scripts/styles to self + Tailwind CDN) and `X-XSS-Protection: 1; mode=block` to all responses.
- **`NoCacheAfterLogoutMiddleware`**: Adds `Cache-Control: no-cache, no-store, must-revalidate` for authenticated sessions to prevent back-button access after logout.

### Email (SendGrid)

`django-sendgrid-v5` is used for:
- Password reset tokens (sent to user's email)
- Novedad notifications (incident alerts)

Configure `SENDGRID_API_KEY` in `.env`.

## Key Conventions

- **Model field naming**: camelCase prefixed by table abbreviation — `usuDocumento`, `vehPlaca`, `espEstado`, `parHoraEntrada`, `pagMonto`, `novDescripcion`, `stkFecha`, etc.
- **Foreign keys**: named `fkId<Entity>` with explicit `db_column` matching — e.g. `fkIdPiso`, `fkIdVehiculo`.
- **All models use explicit `db_table`** in Meta (e.g. `'usuarios'`, `'vehiculos'`, `'espacios'`, `'novedades'`, `'fidelidad_stickers'`).
- **Views are class-based** (`View` subclasses), not DRF ViewSets. CRUD pattern: `<Entity>ListView`, `<Entity>CreateView`, `<Entity>UpdateView`, `<Entity>DeleteView`.
- **No Django Forms** — views read directly from `request.POST`.
- **Derived properties via `@property`**: `Usuario.usuNombreCompleto` (nombre + apellido), `Vehiculo.es_visitante` (True when `fkIdUsuario` is null), `Reserva.resConfirmada`. These are NOT database columns.
- Parking state rule: `InventarioParqueo` with `parHoraSalida IS NULL` means vehicle is currently parked. On exit, the space status flips to `DISPONIBLE` and a `Pago` record is created.
- **Cost calculation**: minute-based — `(minutes / 60) * precioHora`, rounded up to nearest 100 COP. Visitors use `precioHoraVisitante`.
- **Sticker rule**: One `Sticker` is awarded per `InventarioParqueo` record where parking duration > 1 hour (registered users only). When the user accumulates `ConfiguracionFidelidad.metaStickers` stickers, they can redeem them for a 100% discount coupon.

## Validation Strategy (3 layers)

### 1. Model validators (`django.core.validators`)
- `RegexValidator` on text fields: `usuDocumento` (digits only), `usuNombre`/`usuApellido` (letters only), `vehPlaca` (alphanumeric + dash), `cupCodigo` (uppercase alphanumeric), etc.
- `MinValueValidator(0)` on all price/value fields: `precioHora`, `precioHoraVisitante`, `precioDia`, `precioMensual`, `cupValor`.

### 2. Server-side view validation (`re.match()` + `messages.error()`)
- Compiled regex patterns at module level in each views.py (e.g. `RE_SOLO_NUMEROS`, `RE_SOLO_LETRAS`, `RE_PLACA`).
- Views validate input before `save()` and return error messages via Django messages framework.
- Numeric fields use `Decimal` + `InvalidOperation` for safe parsing.

### 3. Frontend HTML5 + JavaScript
- HTML5 attributes: `pattern`, `maxlength`, `minlength`, `min`, `title`, `type="email"/"tel"`.
- JS real-time validation: `input` event listeners toggle red border + error hint text.
- `keypress` blocking on numeric-only fields (documento, teléfono).
- Date validation: fecha fin >= fecha inicio on cupones and tarifas forms.

### Field length limits (max_length)

| Field | max_length | Constraint |
|---|---|---|
| `usuDocumento` | 15 | Digits only |
| `usuNombre` / `usuApellido` | 50 | Letters only |
| `usuTelefono` / `telefono_contacto` | 10 | Digits only |
| `vehPlaca` | 8 | Alphanumeric + dash |
| `vehMarca` / `vehModelo` | 30 | Alphanumeric |
| `vehColor` | 20 | Letters only |
| `cupCodigo` | 20 | Uppercase alphanumeric |
| `cupNombre` / tarifa `nombre` | 50 | Free text |

## Database Models Reference

### usuarios
- `idUsuario` PK, `usuDocumento`, `usuNombre`, `usuApellido` (→ `usuNombreCompleto` property), `usuCorreo`, `usuTelefono`, `usuClaveHash`, `rolTipoRol` ENUM(ADMIN/VIGILANTE/CLIENTE), `usuEstado` bool, `usuFechaRegistro`

### vehiculos
- `idVehiculo` PK, `vehPlaca` (unique), `vehTipo`, `vehColor`, `vehMarca`, `vehModelo`, `fkIdUsuario` (nullable → visitante), `nombre_visitante`, `telefono_contacto`

### parqueadero (pisos, tipos_espacio, espacios, inventario_parqueo)
- `Piso`: `idPiso`, `pisNombre`, `pisEstado`
- `TipoEspacio`: `idTipoEspacio`, `nombre`
- `Espacio`: `idEspacio`, `espNumero`, `fkIdPiso`, `fkIdTipoEspacio`, `espEstado` ENUM(DISPONIBLE/OCUPADO/RESERVADO/INACTIVO)
- `InventarioParqueo`: `idParqueo`, `parHoraEntrada` (auto_now_add), `parHoraSalida` (null=active), `fkIdVehiculo`, `fkIdEspacio`

### tarifas
- `idTarifa`, `nombre`, `fkIdTipoEspacio`, `precioHora`, `precioHoraVisitante`, `precioDia`, `precioMensual`, `activa` bool, `fechaInicio`, `fechaFin` (null=indefinite)

### pagos
- `idPago`, `pagFechaPago` (auto_now_add), `pagMonto`, `pagMetodo`, `pagEstado`, `fkIdParqueo`

### cupones / cupones_aplicados
- `Cupon`: `idCupon`, `cupNombre`, `cupCodigo` (unique uppercase), `cupTipo` (PORCENTAJE/VALOR_FIJO), `cupValor`, `cupDescripcion`, `cupFechaInicio`, `cupFechaFin`, `cupActivo`
- `CuponAplicado`: `idCuponAplicado`, `fkIdPago`, `fkIdCupon`, `montoDescontado`

### reservas
- `idReserva`, `resFechaReserva`, `resHoraInicio`, `resHoraFin`, `resEstado` (PENDIENTE/CONFIRMADA/COMPLETADA/CANCELADA), `fkIdEspacio`, `fkIdVehiculo`

### novedades
- `idNovedad` (auto pk), `novDescripcion` TextField, `novFoto` ImageField (upload_to='novedades/'), `novEstado` (PENDIENTE/EN_PROCESO/RESUELTO), `novComentario` TextField, `fkIdVehiculo` (SET_NULL), `fkIdEspacio` (SET_NULL), `fkIdReportador` (SET_NULL), `fkIdResponsable` (SET_NULL), `novFechaCreacion`, `novFechaActualizacion`

### fidelidad_configuracion / fidelidad_stickers
- `ConfiguracionFidelidad`: singleton (pk=1), `metaStickers` int, `diasVencimientoBono` int
- `Sticker`: `idSticker` (auto pk), `fkIdUsuario` CASCADE, `fkIdParqueo` OneToOne CASCADE, `stkFecha` auto_now_add

## Business Rules

1. A vehicle cannot have more than one active parking entry (`parHoraSalida__isnull=True`).
2. Only `DISPONIBLE` spaces can accept new entries.
3. On vehicle exit: calculate cost from active `Tarifa` (minute-based rate, `precioHoraVisitante` for visitors), create `Pago`, release space.
4. Only one active tariff per `TipoEspacio` at a time.
5. Coupons must be validated for date range before applying.
6. Pisos with occupied spaces cannot be deleted; occupied spaces cannot be deleted.
7. Sticker awarded when registered user parks for more than 1 hour (one sticker per `InventarioParqueo`).
8. When user reaches `metaStickers`, they can claim a coupon for 100% discount valid for `diasVencimientoBono` days.

## Database Management

```bash
# Reset database (drop all tables, recreate migrations, migrate, seed with full demo data)
python scripts/reiniciar_base_datos.py

# Seed test data for Render deployment (PostgreSQL-compatible)
python scripts/render_datos_prueba.py
```

**Migration strategy**: When model changes are significant (field renames, type changes), delete all migration files except `__init__.py`, drop all tables, then run `makemigrations` + `migrate` fresh.

**Database per environment**:
- **Local dev**: MySQL 8.0 (utf8mb4) — configured via `.env` (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
- **Production (Render.com)**: PostgreSQL — configured via `DATABASE_URL` env var, picked up by `dj-database-url`
