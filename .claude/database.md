# Estructura de Base de Datos

Sistema Multiparking

ORM: Django ORM
Motor desarrollo: MySQL 8.0 (utf8mb4)
Motor producción: PostgreSQL (Render.com, via DATABASE_URL + dj-database-url)

---

## 1. Usuarios

Tabla: usuarios

Campos:

- idUsuario (PK)
- usuDocumento (único, solo dígitos, max 15)
- usuNombre (letras, max 50)
- usuApellido (letras, max 50)
- usuCorreo (único)
- usuTelefono (dígitos, max 10)
- usuClaveHash (PBKDF2)
- rolTipoRol ENUM: ADMIN / VIGILANTE / CLIENTE
- usuEstado bool (activo/inactivo)
- usuFechaRegistro auto_now_add

Propiedades (no columnas DB):
- usuNombreCompleto → usuNombre + ' ' + usuApellido

Relaciones:

- 1 Usuario → N Vehículos
- 1 Usuario → N Stickers (fidelidad)
- 1 Usuario → N Novedades (como reportador o responsable)

---

## 2. Vehículos

Tabla: vehiculos

Campos:

- idVehiculo (PK)
- vehPlaca (única, alfanumérico + guión, max 8)
- vehTipo
- vehColor (letras, max 20)
- vehMarca (max 30)
- vehModelo (max 30)
- fkIdUsuario (nullable → visitante)
- nombre_visitante (nullable)
- telefono_contacto (nullable, max 10)

Propiedades (no columnas DB):
- es_visitante → True si fkIdUsuario is null

Relaciones:

- Vehículo → Usuario (opcional)

Reglas:

- Un vehículo no puede tener más de un parqueo activo (parHoraSalida IS NULL).

---

## 3. Pisos

Tabla: pisos

Campos:

- idPiso (PK)
- pisNombre
- pisEstado bool

Relaciones:

- Piso → N Espacios

Reglas:

- No se puede eliminar un piso con espacios ocupados.

---

## 4. Tipos de Espacio

Tabla: tipos_espacio

Campos:

- idTipoEspacio (PK)
- nombre

Ejemplos: Carro, Moto

---

## 5. Espacios

Tabla: espacios

Campos:

- idEspacio (PK)
- espNumero (código alfanumérico, ej: C1-01)
- fkIdPiso
- fkIdTipoEspacio
- espEstado ENUM: DISPONIBLE / OCUPADO / RESERVADO / INACTIVO

Relaciones:

- Espacio → Piso
- Espacio → TipoEspacio

Reglas:

- Solo DISPONIBLE puede aceptar nuevas entradas.
- No se puede eliminar un espacio OCUPADO.

---

## 6. Inventario Parqueo (Ingresos y Salidas)

Tabla: inventario_parqueo

Campos:

- idParqueo (PK)
- parHoraEntrada (auto_now_add — sobreescribir con .update() en scripts)
- parHoraSalida (nullable)
- fkIdVehiculo
- fkIdEspacio

Reglas:

- Si parHoraSalida IS NULL → el vehículo está dentro.
- Al registrar salida → calcular costo → crear Pago → espacio queda DISPONIBLE.
- Cálculo: (minutos / 60) * precioHora, redondeado hacia arriba a 100 COP.
  Visitantes usan precioHoraVisitante de la Tarifa activa.

---

## 7. Tarifas

Tabla: tarifas

Campos:

- idTarifa (PK)
- nombre (max 50)
- fkIdTipoEspacio
- precioHora (Decimal, >= 0)
- precioHoraVisitante (Decimal, >= 0, default 0)
- precioDia (Decimal, >= 0)
- precioMensual (Decimal, >= 0)
- activa bool
- fechaInicio Date
- fechaFin Date (null = vigente indefinidamente)

Relaciones:

- Tarifa → TipoEspacio

Reglas:

- Solo una tarifa activa por tipo de espacio a la vez.

---

## 8. Pagos

Tabla: pagos

Campos:

- idPago (PK)
- pagFechaPago (auto_now_add — sobreescribir con .update() en scripts)
- pagMonto (Decimal)
- pagMetodo
- pagEstado
- fkIdParqueo

Relaciones:

- Pago → InventarioParqueo

---

## 9. Cupones

Tabla: cupones

Campos:

- idCupon (PK)
- cupNombre (max 50)
- cupCodigo (único, mayúsculas alfanumérico, max 20)
- cupTipo ENUM: PORCENTAJE / VALOR_FIJO
- cupValor (Decimal, >= 0)
- cupDescripcion
- cupFechaInicio Date
- cupFechaFin Date
- cupActivo bool

---

## 10. Cupones Aplicados

Tabla: cupones_aplicados

Campos:

- idCuponAplicado (PK)
- fkIdPago
- fkIdCupon
- montoDescontado (Decimal)

Relaciones:

- CuponAplicado → Pago
- CuponAplicado → Cupon

---

## 11. Reservas

Tabla: reservas

Campos:

- idReserva (PK)
- resFechaReserva Date
- resHoraInicio Time
- resHoraFin Time
- resEstado ENUM: PENDIENTE / CONFIRMADA / COMPLETADA / CANCELADA
- fkIdEspacio
- fkIdVehiculo

Propiedades (no columnas DB):
- resConfirmada → True si resEstado == 'CONFIRMADA'

---

## 12. Novedades

Tabla: novedades

Campos:

- idNovedad (auto PK)
- novDescripcion (TextField)
- novFoto (ImageField, upload_to='novedades/', nullable)
- novEstado ENUM: PENDIENTE / EN_PROCESO / RESUELTO
- novComentario (TextField, blank=True) — acciones tomadas / seguimiento
- fkIdVehiculo (SET_NULL, nullable)
- fkIdEspacio (SET_NULL, nullable)
- fkIdReportador (SET_NULL, nullable) → Usuario que reporta
- fkIdResponsable (SET_NULL, nullable) → Usuario responsable de resolver
- novFechaCreacion (auto_now_add)
- novFechaActualizacion (auto_now)

Relaciones:

- Novedad → Vehiculo (opcional)
- Novedad → Espacio (opcional)
- Novedad → Usuario (reportador y responsable)

---

## 13. Fidelidad — Configuración

Tabla: fidelidad_configuracion

Campos:

- id (PK = 1, singleton)
- metaStickers (PositiveInt, default 10) — stickers necesarios para reclamar bono
- diasVencimientoBono (PositiveInt, default 30) — días de validez del cupón bono

Regla: Solo existe un registro (pk=1). Usar ConfiguracionFidelidad.get() para obtenerlo.

---

## 14. Fidelidad — Stickers

Tabla: fidelidad_stickers

Campos:

- id (auto PK)
- fkIdUsuario (CASCADE) → Usuario que gana el sticker
- fkIdParqueo (OneToOne, CASCADE) → InventarioParqueo que generó el sticker
- stkFecha (auto_now_add)

Reglas:

- Un sticker por InventarioParqueo (OneToOne).
- Solo se genera si la duración del parqueo fue > 1 hora.
- Solo para usuarios registrados (no visitantes).

---

# Reglas Globales

1. No permitir ingreso si el vehículo ya tiene un parqueo activo (parHoraSalida IS NULL).
2. No asignar espacios en estado distinto a DISPONIBLE.
3. Al registrar salida:
   - Calcular valor según tarifa activa (precioHoraVisitante para visitantes).
   - Registrar pago.
   - Liberar el espacio (DISPONIBLE).
   - Evaluar si corresponde otorgar sticker.
4. Validar vigencia de cupones antes de aplicar.
5. Solo una tarifa activa por TipoEspacio a la vez.
6. No eliminar pisos con espacios ocupados; no eliminar espacios ocupados.
