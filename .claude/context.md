# CONTEXTO DEL PROYECTO

## Descripción General

Sistema web para la gestión integral de un parqueadero desarrollado en Django 6.0 (Python 3.12+).

Permite administrar:

- Usuarios (Admin, Vigilante, Cliente)
- Vehículos (registrados y visitantes)
- Pisos y espacios de parqueo
- Tipos de espacio
- Tarifas (con precio diferenciado visitante)
- Ingresos y salidas
- Reservas (admin y cliente)
- Pagos
- Cupones de descuento
- Novedades / Incidentes
- Programa de fidelidad (stickers)
- Control en tiempo real
- Reportes PDF y Excel

El sistema es:

- Seguro (CSP, no-cache, PBKDF2, recuperación por email)
- Escalable
- Modular (9 apps Django)
- Corporativo
- Operación en tiempo real

---

# STACK TECNOLÓGICO

## Backend

- Django 6.0.2
- Django REST Framework
- Arquitectura MVT + class-based views
- Autenticación por Sesión personalizada (sin django.contrib.auth.User)
- MySQL 8.0 en desarrollo / PostgreSQL en producción (Render.com)
- dj-database-url para DATABASE_URL en producción
- SendGrid (django-sendgrid-v5) para emails

## Frontend

- Django Templates
- Tailwind CSS (CDN)
- Responsive
- Panel administrativo moderno Dark Mode

## Exportaciones

- reportlab → PDF
- openpyxl → Excel

---

# ARQUITECTURA

Apps:

- usuarios
- vehiculos
- parqueadero
- tarifas
- pagos
- cupones
- reservas
- novedades
- fidelidad

Separación de vistas:

- `views.py` → vistas admin/principal
- `vigilante_views.py` → vistas exclusivas del guardia (parqueadero)
- `cliente_views.py` → self-service del cliente (vehiculos, reservas, parqueadero)
- `reportes_views.py` → exportaciones PDF/Excel (parqueadero)

Reglas:

- CRUD con class-based views (no DRF ViewSets)
- Validación directa en views (no Django Forms)
- Manejo de errores vía messages framework

---

# ROLES (ENUM rolTipoRol)

- ADMIN → control total del panel admin
- VIGILANTE → panel guardia: registrar ingresos/salidas
- CLIENTE → dashboard propio, vehículos, reservas, perfil fidelidad

No existe tabla de roles separada — el ENUM está en el modelo Usuario.

---

# MÓDULOS

## Usuarios

Documento, Nombre, Apellido, Email, Teléfono, Clave hash, Rol, Estado.
Recuperación de contraseña vía email (SendGrid, token de un solo uso).

## Vehículos

Placa única. Un vehículo no puede tener más de un parqueo activo.
Soporta visitantes (fkIdUsuario null + nombre_visitante + telefono_contacto).

## Pisos

Contienen múltiples espacios.

## Tipos de Espacio

Clasificación física y asociación de tarifas.

## Espacios

Estado: DISPONIBLE / OCUPADO / RESERVADO / INACTIVO

## Tarifas

Una tarifa pertenece a un TipoEspacio. Solo una activa por tipo y fecha.
Tiene precioHora (usuario registrado) y precioHoraVisitante (visitante sin cuenta).

## Inventario Parqueo

Si parHoraSalida IS NULL → vehículo activo. Salida → calcular valor → liberar espacio.
El cálculo usa precioHoraVisitante para vehículos de visitantes.

## Reservas

Bloquean espacios durante rango horario.
Gestionadas por admin y por el propio cliente.

## Pagos

Generados automáticamente al registrar salida.

## Cupones

Validar vigencia antes de aplicar.
Identificados por código único (cupCodigo).

## Novedades

Incidentes o eventos asociados a un vehículo y/o espacio.
Estados: PENDIENTE, EN_PROCESO, RESUELTO.
Soporta foto adjunta.

## Fidelidad

Sistema de stickers: un sticker por parqueo > 1 hora (usuarios registrados).
Al alcanzar la meta (metaStickers), el cliente puede reclamar un cupón de 100% con vigencia configurable.
ConfiguracionFidelidad es un singleton (pk=1).

---

# OBJETIVO

Sistema robusto para control eficiente, trazabilidad y escalabilidad de parqueaderos multinivel.
