# CONTEXTO DEL PROYECTO

## Descripción General

Sistema web para la gestión integral de un parqueadero desarrollado en

Django.

Permite administrar:

- Usuarios
- Vehículos
- Pisos
- Espacios
- Tipos de espacio
- Tarifas
- Ingresos y salidas
- Reservas
- Pagos
- Cupones
- Control en tiempo real

El sistema debe ser:

- Seguro
- Escalable
- Modular
- Corporativo
- Operación en tiempo real

---

# STACK TECNOLÓGICO

## Backend

- Django
- Django REST Framework
- Arquitectura REST
- Autenticación por Sesión o JWT
- MySQL / PostgreSQL

## Frontend

- Django Templates
- Tailwind CSS
- Responsive
- Panel administrativo moderno

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

Separación:

- models → estructura
- serializers → validación
- views/viewsets → endpoints
- services → reglas complejas
- urls → rutas

Reglas:

- CRUD REST
- Validaciones en serializers
- Manejo centralizado de errores

---

# ROLES (ENUM rolTipoRol)

- ADMIN → control total
- VIGILANTE → operación diaria
- CLIENTE → gestión propia

No existe tabla de roles.

---

# MÓDULOS

## Usuarios

Documento, Nombre, Email, Teléfono, Clave hash, Rol, Estado.

## Vehículos

Placa única. Un vehículo no puede tener más de un parqueo activo.

## Pisos

Contienen múltiples espacios.

## Tipos de Espacio

Clasificación física y asociación de tarifas.

## Espacios

Estado: - DISPONIBLE - OCUPADO - INACTIVO

## Tarifas

Una tarifa pertenece a un TipoEspacio. Solo una activa por tipo y fecha.

## Inventario Parqueo

Si parHoraSalida IS NULL → vehículo activo. Salida → calcular valor →

liberar espacio.

## Reservas

Bloquean espacios durante rango horario.

## Pagos

Generados automáticamente al salir.

## Cupones

Validar vigencia antes de aplicar.

---

# OBJETIVO

Sistema robusto para control eficiente, trazabilidad y escalabilidad.

# ESTRUCTURA DE BASE DE DATOS

## 1. usuarios

- idUsuario (PK)
- usuDocumento
- usuNombreCompleto
- usuCorreo
- usuTelefono
- usuClaveHash
- rolTipoRol (ADMIN, VIGILANTE, CLIENTE)
- usuEstado
- usuFechaRegistro

Relación: Usuario → N Vehículos

---

## 2. vehiculos

- idVehiculo (PK)
- vehPlaca (única)
- vehTipo
- vehColor
- vehMarca
- vehModelo
- fkIdUsuario

Regla: Un vehículo no puede tener más de un parqueo activo.

---

## 3. pisos

- idPiso (PK)
- pisNombre
- pisEstado

---

## 4. tipos_espacio

- idTipoEspacio (PK)
- nombre

---

## 5. espacios

- idEspacio (PK)
- espNumero
- fkIdPiso
- fkIdTipoEspacio
- espEstado (DISPONIBLE, OCUPADO, INACTIVO)

---

## 6. inventario_parqueo

- idParqueo (PK)
- parHoraEntrada
- parHoraSalida
- fkIdVehiculo
- fkIdEspacio

Regla: parHoraSalida NULL → activo.

---

## 7. reservas

- idReserva (PK)
- resFechaReserva
- resHoraInicio
- resHoraFin
- resEstado
- fkIdEspacio
- fkIdVehiculo

---

## 8. tarifas

- idTarifa (PK)
- nombre
- fkIdTipoEspacio
- precioHora
- precioDia
- precioMensual
- activa
- fechaInicio
- fechaFin

Regla: Una tarifa activa por tipo y fecha.

---

## 9. pagos

- idPago (PK)
- pagFechaPago
- pagMonto
- pagMetodo
- pagEstado
- fkIdParqueo

---

## 10. cupones

- idCupon
- cupNombre
- cupTipo
- cupValor
- cupDescripcion
- cupFechaInicio
- cupFechaFin
- cupActivo

---

## 11. cupones_aplicados

- idCuponAplicado
- fkIdPago
- fkIdCupon
- montoDescontado

---

# REGLAS GLOBALES

1. No ingreso si vehículo ya activo.
2. No asignar espacio ocupado.
3. Salida → calcular tarifa → registrar pago → liberar espacio.
4. Validar vigencia de cupones.
