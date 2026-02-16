# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Multiparking** — a Django web application for managing a multi-floor parking lot. Handles users, vehicles, parking spaces, entry/exit tracking, reservations, tariffs, payments, and discount coupons.

Language: Spanish for business-domain names, English for framework/technical terms.

## Development Commands

```bash
# Install dependencies (requires MySQL client libraries)
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
```

## Architecture

### Django Project: `multiparking/`
Settings module. Uses MySQL (utf8mb4), timezone `America/Bogota`, locale `es-co`. Env vars loaded via `python-dotenv`.

### Apps

| App | Responsibility |
|---|---|
| `usuarios` | Custom `Usuario` model (NOT Django's auth User), login/register/logout views, session management, `AdminRequiredMixin` |
| `vehiculos` | `Vehiculo` model — supports both registered users and visitors (`es_visitante` flag) |
| `parqueadero` | Core parking logic: `Piso`, `TipoEspacio`, `Espacio`, `InventarioParqueo`. All admin panel CRUD views. Entry/exit operations |
| `tarifas` | `Tarifa` model — pricing per hour/day/month linked to `TipoEspacio` |
| `pagos` | `Pago` model — payment records linked to `InventarioParqueo` |
| `cupones` | `Cupon` and `CuponAplicado` models — discount coupons (percentage or fixed value) |
| `reservas` | `Reserva` model — space reservations by date/time |

### Authentication & Authorization

- **Custom session-based auth** — does NOT use `django.contrib.auth` User model. The `Usuario` model stores `usuClaveHash` (hashed with `django.contrib.auth.hashers`).
- Session keys: `usuario_id`, `usuario_nombre`, `usuario_rol`, `usuario_correo`.
- Three roles via `rolTipoRol` ENUM: `ADMIN`, `VIGILANTE`, `CLIENTE`.
- Admin-only views use `AdminRequiredMixin` (in `usuarios/mixins.py`) which checks session role.

### URL Structure

- `/` — public home, `/login/`, `/register/`, `/logout/`
- `/dashboard/` — client dashboard
- `/admin-panel/` — admin dashboard and all CRUD views (`/admin-panel/pisos/`, `/admin-panel/espacios/`, etc.)
- `/api/<app>/` — REST API endpoints (DRF is installed but serializers are not yet implemented)

### Frontend

- Server-side rendering with Django Templates + Tailwind CSS (via CDN).
- Templates in `templates/` root directory: `base.html`, `home.html`, `auth/`, `admin_panel/`.
- `admin_panel/base.html` is the layout for all admin views; each view passes `active_page` for sidebar highlighting.
- AJAX calls use `X-Requested-With: XMLHttpRequest` header; views return `JsonResponse` for AJAX, rendered HTML otherwise.

## Key Conventions

- **Model field naming**: camelCase prefixed by table abbreviation — `usuDocumento`, `vehPlaca`, `espEstado`, `parHoraEntrada`, `pagMonto`, etc.
- **Foreign keys**: named `fkId<Entity>` with explicit `db_column` matching — e.g. `fkIdPiso`, `fkIdVehiculo`.
- **All models use explicit `db_table`** in Meta (e.g. `'usuarios'`, `'vehiculos'`, `'espacios'`).
- **Views are class-based** (`View` subclasses), not DRF ViewSets. CRUD pattern: `<Entity>ListView`, `<Entity>CreateView`, `<Entity>UpdateView`, `<Entity>DeleteView`.
- **No Django Forms** — views read directly from `request.POST`.
- Parking state rule: `InventarioParqueo` with `parHoraSalida IS NULL` means vehicle is currently parked. On exit, the space status flips to `DISPONIBLE` and a `Pago` record is created.

## Business Rules

1. A vehicle cannot have more than one active parking entry (`parHoraSalida__isnull=True`).
2. Only `DISPONIBLE` spaces can accept new entries.
3. On vehicle exit: calculate cost from active `Tarifa` (hourly rate, rounded up), create `Pago`, release space.
4. Only one active tariff per `TipoEspacio` at a time.
5. Coupons must be validated for date range before applying.
6. Pisos with occupied spaces cannot be deleted; occupied spaces cannot be deleted.
