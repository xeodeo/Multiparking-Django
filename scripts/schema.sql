-- ============================================================
-- MULTIPARKING - Script de creación de base de datos
-- Solo tablas del proyecto (sin tablas internas de Django)
-- Motor: MySQL / MariaDB | Charset: utf8mb4
-- ============================================================

CREATE DATABASE IF NOT EXISTS multiparking
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE multiparking;

SET FOREIGN_KEY_CHECKS = 0;

-- ────────────────────────────────────────────────────────────
-- 1. USUARIOS
-- ────────────────────────────────────────────────────────────
CREATE TABLE usuarios (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    usuDocumento    VARCHAR(15)  NOT NULL,
    usuNombre       VARCHAR(50)  NOT NULL,
    usuApellido     VARCHAR(50)  NOT NULL,
    usuCorreo       VARCHAR(254) NOT NULL,
    usuTelefono     VARCHAR(10)  NOT NULL DEFAULT '',
    usuClaveHash    VARCHAR(255) NOT NULL,
    rolTipoRol      ENUM('ADMIN', 'VIGILANTE', 'CLIENTE') NOT NULL DEFAULT 'CLIENTE',
    usuEstado       TINYINT(1)   NOT NULL DEFAULT 1,
    usuFechaRegistro DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_usuario_documento UNIQUE (usuDocumento),
    CONSTRAINT uq_usuario_correo    UNIQUE (usuCorreo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 2. VEHICULOS
-- ────────────────────────────────────────────────────────────
CREATE TABLE vehiculos (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    vehPlaca           VARCHAR(8)   NOT NULL,
    vehTipo            ENUM('Carro', 'Moto') NOT NULL DEFAULT 'Carro',
    vehColor           VARCHAR(20)  NOT NULL DEFAULT '',
    vehMarca           VARCHAR(30)  NOT NULL DEFAULT '',
    vehModelo          VARCHAR(30)  NOT NULL DEFAULT '',
    vehEstado          TINYINT(1)   NOT NULL DEFAULT 1,
    fkIdUsuario        INT          NULL,
    nombre_contacto    VARCHAR(50)  NULL,
    telefono_contacto  VARCHAR(10)  NULL,

    CONSTRAINT uq_vehiculo_placa    UNIQUE (vehPlaca),
    CONSTRAINT fk_vehiculo_usuario  FOREIGN KEY (fkIdUsuario) REFERENCES usuarios(id) ON DELETE CASCADE,

    INDEX idx_vehiculo_placa (vehPlaca)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 3. PISOS
-- ────────────────────────────────────────────────────────────
CREATE TABLE pisos (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    pisNombre VARCHAR(30)  NOT NULL,
    pisEstado TINYINT(1)   NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 4. TIPOS DE ESPACIO
-- ────────────────────────────────────────────────────────────
CREATE TABLE tipos_espacio (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,

    CONSTRAINT uq_tipo_espacio_nombre UNIQUE (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 5. ESPACIOS
-- ────────────────────────────────────────────────────────────
CREATE TABLE espacios (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    espNumero       VARCHAR(10) NOT NULL,
    fkIdPiso        INT         NOT NULL,
    fkIdTipoEspacio INT         NOT NULL,
    espEstado       ENUM('DISPONIBLE', 'OCUPADO', 'INACTIVO') NOT NULL DEFAULT 'DISPONIBLE',

    CONSTRAINT fk_espacio_piso         FOREIGN KEY (fkIdPiso)        REFERENCES pisos(id)         ON DELETE CASCADE,
    CONSTRAINT fk_espacio_tipo_espacio FOREIGN KEY (fkIdTipoEspacio) REFERENCES tipos_espacio(id) ON DELETE CASCADE,
    CONSTRAINT uq_espacio_piso_numero  UNIQUE (fkIdPiso, espNumero),

    INDEX idx_espacio_numero (espNumero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 6. INVENTARIO PARQUEO (entradas/salidas)
-- ────────────────────────────────────────────────────────────
CREATE TABLE inventario_parqueo (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    parHoraEntrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parHoraSalida  DATETIME NULL,
    fkIdVehiculo   INT      NOT NULL,
    fkIdEspacio    INT      NOT NULL,

    CONSTRAINT fk_parqueo_vehiculo FOREIGN KEY (fkIdVehiculo) REFERENCES vehiculos(id) ON DELETE CASCADE,
    CONSTRAINT fk_parqueo_espacio  FOREIGN KEY (fkIdEspacio)  REFERENCES espacios(id)  ON DELETE CASCADE,

    INDEX idx_parqueo_estado (parHoraSalida)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 7. TARIFAS
-- ────────────────────────────────────────────────────────────
CREATE TABLE tarifas (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    nombre              VARCHAR(50)    NOT NULL,
    fkIdTipoEspacio     INT            NOT NULL,
    precioHora          DECIMAL(10,2)  NOT NULL,
    precioHoraVisitante DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    precioDia           DECIMAL(10,2)  NOT NULL,
    precioMensual       DECIMAL(12,2)  NOT NULL,
    activa              TINYINT(1)     NOT NULL DEFAULT 1,
    fechaInicio         DATE           NOT NULL,
    fechaFin            DATE           NULL,

    CONSTRAINT fk_tarifa_tipo_espacio FOREIGN KEY (fkIdTipoEspacio) REFERENCES tipos_espacio(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 8. PAGOS
-- ────────────────────────────────────────────────────────────
CREATE TABLE pagos (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    pagFechaPago DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pagMonto     DECIMAL(12,2) NOT NULL,
    pagMetodo    ENUM('EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'PSE') NOT NULL DEFAULT 'EFECTIVO',
    pagEstado    ENUM('PENDIENTE', 'PAGADO', 'ANULADO')              NOT NULL DEFAULT 'PENDIENTE',
    fkIdParqueo  INT           NOT NULL,

    CONSTRAINT fk_pago_parqueo FOREIGN KEY (fkIdParqueo) REFERENCES inventario_parqueo(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 9. CUPONES
-- ────────────────────────────────────────────────────────────
CREATE TABLE cupones (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    cupNombre      VARCHAR(50)   NOT NULL,
    cupCodigo      VARCHAR(20)   NOT NULL,
    cupTipo        ENUM('PORCENTAJE', 'VALOR_FIJO') NOT NULL,
    cupValor       DECIMAL(10,2) NOT NULL,
    cupDescripcion TEXT,
    cupFechaInicio DATE          NOT NULL,
    cupFechaFin    DATE          NOT NULL,
    cupActivo      TINYINT(1)    NOT NULL DEFAULT 1,

    CONSTRAINT uq_cupon_codigo UNIQUE (cupCodigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 10. CUPONES APLICADOS (relación Pago ↔ Cupón)
-- ────────────────────────────────────────────────────────────
CREATE TABLE cupones_aplicados (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    fkIdPago         INT           NOT NULL,
    fkIdCupon        INT           NOT NULL,
    montoDescontado  DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_cupon_aplicado_pago  FOREIGN KEY (fkIdPago)  REFERENCES pagos(id)   ON DELETE CASCADE,
    CONSTRAINT fk_cupon_aplicado_cupon FOREIGN KEY (fkIdCupon) REFERENCES cupones(id)  ON DELETE CASCADE,
    CONSTRAINT uq_cupon_aplicado       UNIQUE (fkIdPago, fkIdCupon)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ────────────────────────────────────────────────────────────
-- 11. RESERVAS
-- ────────────────────────────────────────────────────────────
CREATE TABLE reservas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    resFechaReserva DATE        NOT NULL,
    resHoraInicio   TIME        NOT NULL,
    resHoraFin      TIME        NULL,
    resEstado       ENUM('PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA') NOT NULL DEFAULT 'PENDIENTE',
    fkIdEspacio     INT         NOT NULL,
    fkIdVehiculo    INT         NOT NULL,

    CONSTRAINT fk_reserva_espacio  FOREIGN KEY (fkIdEspacio)  REFERENCES espacios(id)  ON DELETE CASCADE,
    CONSTRAINT fk_reserva_vehiculo FOREIGN KEY (fkIdVehiculo) REFERENCES vehiculos(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- FIN DEL SCRIPT
-- 11 tablas creadas | 0 tablas de Django
-- ============================================================
