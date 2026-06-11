-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-11-2025 a las 12:57:04
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `multiparking`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cupones`
--

CREATE TABLE `cupones` (
  `idCupon` int(11) NOT NULL,
  `cupNombre` varchar(100) NOT NULL,
  `cupTipo` enum('PORCENTAJE','VALOR_FIJO') NOT NULL,
  `cupValor` decimal(10,2) NOT NULL,
  `cupDescripcion` text DEFAULT NULL,
  `cupCondicion` varchar(255) DEFAULT NULL,
  `cupFechaInicio` date DEFAULT NULL,
  `cupFechaFin` date DEFAULT NULL,
  `cupActivo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cupones_aplicados`
--

CREATE TABLE `cupones_aplicados` (
  `idCuponAplicado` int(11) NOT NULL,
  `fkIdPago` int(11) NOT NULL,
  `fkIdCupon` int(11) NOT NULL,
  `montoDescontado` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `espacios`
--

CREATE TABLE `espacios` (
  `idEspacio` int(11) NOT NULL,
  `espNumero` varchar(25) NOT NULL,
  `espPiso` varchar(25) NOT NULL,
  `espTipo` varchar(50) NOT NULL,
  `espEstado` enum('DISPONIBLE','OCUPADO','RESERVADO','INACTIVO') NOT NULL DEFAULT 'DISPONIBLE',
  `espValorTarifa` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_parqueos`
--

CREATE TABLE `inventario_parqueos` (
  `idParqueo` int(11) NOT NULL,
  `parHoraEntrada` timestamp NOT NULL DEFAULT current_timestamp(),
  `parHoraSalida` timestamp NULL DEFAULT NULL,
  `fkIdVehiculo` int(11) NOT NULL,
  `fkIdEspacio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `novedades`
--

CREATE TABLE `novedades` (
  `idNovedad` int(11) NOT NULL,
  `fkIdUsuario` int(11) NOT NULL,
  `fkIdParqueo` int(11) DEFAULT NULL,
  `fkIdVehiculo` int(11) DEFAULT NULL,
  `novDescripcion` text NOT NULL,
  `novFechaHora` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `idPago` int(11) NOT NULL,
  `pagFechaPago` timestamp NOT NULL DEFAULT current_timestamp(),
  `pagMonto` decimal(10,2) NOT NULL,
  `pagMetodo` enum('EFECTIVO','NEQUI','TARJETA','DAVIPLATA') NOT NULL,
  `pagEstado` enum('PENDIENTE','PAGADO','CANCELADO') DEFAULT 'PENDIENTE',
  `fkIdParqueo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `idReserva` int(11) NOT NULL,
  `resFechaReserva` date NOT NULL,
  `resHoraInicio` datetime NOT NULL,
  `resEstado` enum('RESERVADO','CANCELADO','FINALIZADO') DEFAULT 'RESERVADO',
  `fkIdEspacio` int(11) DEFAULT NULL,
  `fkIdVehiculo` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL,
  `usuDocumento` varchar(50) NOT NULL,
  `usuNombreCompleto` varchar(255) NOT NULL,
  `usuCorreo` varchar(255) DEFAULT NULL,
  `usuTelefono` varchar(50) DEFAULT NULL,
  `usuClaveHash` varchar(255) NOT NULL,
  `rolTipoRol` enum('ADMINISTRADOR','CELADOR','USUARIO') NOT NULL,
  `usuEstado` enum('ACTIVO','INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  `usuFechaRegistro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE `vehiculos` (
  `idVehiculo` int(11) NOT NULL,
  `vehPlaca` varchar(50) NOT NULL,
  `vehTipo` varchar(50) NOT NULL,
  `vehColor` varchar(50) DEFAULT NULL,
  `vehMarca` varchar(50) DEFAULT NULL,
  `vehModelo` varchar(50) DEFAULT NULL,
  `fkIdUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cupones`
--
ALTER TABLE `cupones`
  ADD PRIMARY KEY (`idCupon`);

--
-- Indices de la tabla `cupones_aplicados`
--
ALTER TABLE `cupones_aplicados`
  ADD PRIMARY KEY (`idCuponAplicado`),
  ADD KEY `fk_cupon_pago` (`fkIdPago`),
  ADD KEY `fk_cupon_cupon` (`fkIdCupon`);

--
-- Indices de la tabla `espacios`
--
ALTER TABLE `espacios`
  ADD PRIMARY KEY (`idEspacio`);

--
-- Indices de la tabla `inventario_parqueos`
--
ALTER TABLE `inventario_parqueos`
  ADD PRIMARY KEY (`idParqueo`),
  ADD KEY `fk_parqueo_vehiculo` (`fkIdVehiculo`),
  ADD KEY `fk_parqueo_espacio` (`fkIdEspacio`);

--
-- Indices de la tabla `novedades`
--
ALTER TABLE `novedades`
  ADD PRIMARY KEY (`idNovedad`),
  ADD KEY `fk_nov_usu` (`fkIdUsuario`),
  ADD KEY `fk_nov_parq` (`fkIdParqueo`),
  ADD KEY `fk_nov_veh` (`fkIdVehiculo`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`idPago`),
  ADD KEY `fk_pago_parqueo` (`fkIdParqueo`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`idReserva`),
  ADD KEY `fk_reserva_espacio` (`fkIdEspacio`),
  ADD KEY `fk_reserva_vehiculo` (`fkIdVehiculo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `usuDocumento` (`usuDocumento`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`idVehiculo`),
  ADD UNIQUE KEY `vehPlaca` (`vehPlaca`),
  ADD KEY `fk_vehiculo_usuario` (`fkIdUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cupones`
--
ALTER TABLE `cupones`
  MODIFY `idCupon` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cupones_aplicados`
--
ALTER TABLE `cupones_aplicados`
  MODIFY `idCuponAplicado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `espacios`
--
ALTER TABLE `espacios`
  MODIFY `idEspacio` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario_parqueos`
--
ALTER TABLE `inventario_parqueos`
  MODIFY `idParqueo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `novedades`
--
ALTER TABLE `novedades`
  MODIFY `idNovedad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `idPago` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `idReserva` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  MODIFY `idVehiculo` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cupones_aplicados`
--
ALTER TABLE `cupones_aplicados`
  ADD CONSTRAINT `fk_cupon_cupon` FOREIGN KEY (`fkIdCupon`) REFERENCES `cupones` (`idCupon`),
  ADD CONSTRAINT `fk_cupon_pago` FOREIGN KEY (`fkIdPago`) REFERENCES `pagos` (`idPago`);

--
-- Filtros para la tabla `inventario_parqueos`
--
ALTER TABLE `inventario_parqueos`
  ADD CONSTRAINT `fk_parqueo_espacio` FOREIGN KEY (`fkIdEspacio`) REFERENCES `espacios` (`idEspacio`),
  ADD CONSTRAINT `fk_parqueo_vehiculo` FOREIGN KEY (`fkIdVehiculo`) REFERENCES `vehiculos` (`idVehiculo`);

--
-- Filtros para la tabla `novedades`
--
ALTER TABLE `novedades`
  ADD CONSTRAINT `fk_nov_parq` FOREIGN KEY (`fkIdParqueo`) REFERENCES `inventario_parqueos` (`idParqueo`),
  ADD CONSTRAINT `fk_nov_usu` FOREIGN KEY (`fkIdUsuario`) REFERENCES `usuarios` (`idUsuario`),
  ADD CONSTRAINT `fk_nov_veh` FOREIGN KEY (`fkIdVehiculo`) REFERENCES `vehiculos` (`idVehiculo`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `fk_pago_parqueo` FOREIGN KEY (`fkIdParqueo`) REFERENCES `inventario_parqueos` (`idParqueo`);

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `fk_reserva_espacio` FOREIGN KEY (`fkIdEspacio`) REFERENCES `espacios` (`idEspacio`),
  ADD CONSTRAINT `fk_reserva_vehiculo` FOREIGN KEY (`fkIdVehiculo`) REFERENCES `vehiculos` (`idVehiculo`);

--
-- Filtros para la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD CONSTRAINT `fk_vehiculo_usuario` FOREIGN KEY (`fkIdUsuario`) REFERENCES `usuarios` (`idUsuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
