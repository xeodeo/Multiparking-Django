# Estructura de Base de Datos

Sistema Multiparking

ORM: Django ORM
Motor: MySQL / PostgreSQL

---

## 1. Usuarios

Tabla: usuarios

Campos:

- idUsuario (PK)
- usuDocumento
- usuNombreCompleto
- usuCorreo
- usuTelefono
- usuClaveHash
- rolTipoRol ENUM:
  - ADMIN
  - VIGILANTE
  - CLIENTE
- usuEstado (activo/inactivo)
- usuFechaRegistro

Relaciones:

- 1 Usuario → N Vehículos

---

## 2. Vehículos

Tabla: vehiculos

Campos:

- idVehiculo (PK)
- vehPlaca (única)
- vehTipo
- vehColor
- vehMarca
- vehModelo
- fkIdUsuario

Relaciones:

- Vehículo → Usuario

Reglas:

- Un vehículo no puede tener más de un parqueo activo.

---

## 3. Pisos

Tabla: pisos

Campos:

- idPiso (PK)
- pisNombre
- pisEstado

Relaciones:

- Piso → N Espacios

---

## 4. Tipos de Espacio

Tabla: tipos_espacio

Campos:

- idTipoEspacio (PK)
- nombre

Ejemplos:

- CARRO
- MOTO
- DISCAPACITADOS
- VISITANTE

---

## 5. Espacios

Tabla: espacios

Campos:

- idEspacio (PK)
- espNumero
- fkIdPiso
- fkIdTipoEspacio
- espEstado ENUM:
  - DISPONIBLE
  - OCUPADO
  - INACTIVO

Relaciones:

- Espacio → Piso
- Espacio → TipoEspacio

---

## 6. Inventario Parqueo (Ingresos y Salidas)

Tabla: inventario_parqueo

Campos:

- idParqueo (PK)
- parHoraEntrada
- parHoraSalida (nullable)
- fkIdVehiculo
- fkIdEspacio

Reglas:

- Si parHoraSalida es NULL → el vehículo está dentro.
- Al registrar salida → el espacio debe quedar DISPONIBLE.

---

## 7. Reservas

Tabla: reservas

Campos:

- idReserva (PK)
- resFechaReserva
- resHoraInicio
- resHoraFin
- resEstado
- fkIdEspacio
- fkIdVehiculo

---

## 8. Tarifas

Tabla: tarifas

Campos:

- idTarifa (PK)
- nombre
- fkIdTipoEspacio
- precioHora
- precioDia
- precioMensual
- activa
- fechaInicio
- fechaFin

Relaciones:

- Tarifa → TipoEspacio

Reglas:

- Solo una tarifa activa por tipo de espacio en una fecha.

---

## 9. Pagos

Tabla: pagos

Campos:

- idPago (PK)
- pagFechaPago
- pagMonto
- pagMetodo
- pagEstado
- fkIdParqueo

Relaciones:

- Pago → InventarioParqueo

---

## 10. Cupones

Tabla: cupones

Campos:

- idCupon
- cupNombre
- cupTipo
- cupValor
- cupDescripcion
- cupFechaInicio
- cupFechaFin
- cupActivo

---

## 11. Cupones Aplicados

Tabla: cupones_aplicados

Campos:

- idCuponAplicado
- fkIdPago
- fkIdCupon
- montoDescontado

Relaciones:

- CupónAplicado → Pago
- CupónAplicado → Cupón

---

# Reglas Globales

1. No permitir ingreso si el vehículo ya tiene un parqueo activo.
2. No asignar espacios ocupados.
3. Al registrar salida:
   - Calcular valor según tarifa.
   - Registrar pago.
   - Liberar el espacio.
4. Validar vigencia de cupones.
