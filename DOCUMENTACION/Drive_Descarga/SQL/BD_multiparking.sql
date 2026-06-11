-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3340
-- Tiempo de generación: 24-06-2025 a las 18:39:52
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
-- Estructura de tabla para la tabla `descuentos`
--

CREATE TABLE `descuentos` (
  `idDescuento` int(11) NOT NULL,
  `desNombre` varchar(100) NOT NULL,
  `desTipo` enum('porcentaje','valor_fijo') NOT NULL,
  `desValor` decimal(10,2) NOT NULL,
  `desDescripcion` text DEFAULT NULL,
  `desCondicion` varchar(255) DEFAULT NULL,
  `desFechaInicio` date DEFAULT NULL,
  `desFechaFin` date DEFAULT NULL,
  `desActivo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `descuentos`
--

INSERT INTO `descuentos` (`idDescuento`, `desNombre`, `desTipo`, `desValor`, `desDescripcion`, `desCondicion`, `desFechaInicio`, `desFechaFin`, `desActivo`) VALUES
(1, 'Descuento 10%', 'porcentaje', 10.00, '10% general', '*', '2025-06-11', '2025-07-11', 1),
(2, 'Promo Festiva', 'valor_fijo', 2000.00, 'Días festivos', '*', '2025-06-11', '2025-07-11', 1),
(3, 'Cliente Frecuente', 'porcentaje', 15.00, 'Clientes con más de 10 visitas', 'frecuente', '2025-06-11', '2025-07-11', 1),
(4, 'Descuento Moto', 'valor_fijo', 1000.00, 'Solo motos', 'moto', '2025-06-11', '2025-07-11', 1),
(5, 'Convenio Empresa', 'porcentaje', 20.00, 'Aliado empresarial', 'empresa', '2025-06-11', '2025-07-11', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `descuentos_aplicados`
--

CREATE TABLE `descuentos_aplicados` (
  `idDescuentoAplicado` int(11) NOT NULL,
  `fkIdPago` int(11) NOT NULL,
  `fkIdDescuento` int(11) NOT NULL,
  `montoDescontado` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `descuentos_aplicados`
--

INSERT INTO `descuentos_aplicados` (`idDescuentoAplicado`, `fkIdPago`, `fkIdDescuento`, `montoDescontado`) VALUES
(1, 1, 1, 500.00),
(2, 2, 2, 2000.00),
(3, 3, 3, 1050.00),
(4, 4, 4, 1000.00),
(5, 5, 5, 1840.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `idPago` int(11) NOT NULL,
  `pagFechaPago` timestamp NOT NULL DEFAULT current_timestamp(),
  `pagMonto` decimal(10,2) DEFAULT NULL,
  `pagMetodo` varchar(100) DEFAULT NULL,
  `pagEstado` varchar(100) DEFAULT NULL,
  `fkIdParqueo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`idPago`, `pagFechaPago`, `pagMonto`, `pagMetodo`, `pagEstado`, `fkIdParqueo`) VALUES
(1, '2025-06-20 05:00:00', 5000.00, 'Efectivo', 'Pagado', 1),
(2, '2025-06-19 05:00:00', 3000.00, 'Tarjeta', 'Pagado', 2),
(3, '2025-06-18 05:00:00', 7000.00, 'Nequi', 'Pendiente', 3),
(4, '2025-06-17 05:00:00', 2400.00, 'Daviplata', 'Pagado', 4),
(5, '2025-06-16 05:00:00', 9200.00, 'Tarjeta', 'Pagado', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parqueos`
--

CREATE TABLE `parqueos` (
  `idParqueo` int(11) NOT NULL,
  `parPiso` int(11) DEFAULT NULL,
  `parNumeroEspacio` int(11) DEFAULT NULL,
  `parTipoVehiculo` varchar(50) DEFAULT NULL,
  `parEstadoEspacio` enum('DISPONIBLE','OCUPADO') DEFAULT NULL,
  `parHoraEntrada` timestamp NOT NULL DEFAULT current_timestamp(),
  `parHoraSalida` timestamp NULL DEFAULT NULL,
  `parEstado` enum('ACTIVO','INACTIVO') DEFAULT 'ACTIVO',
  `fkIdVehiculo` int(11) NOT NULL,
  `fkIdTarifa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `parqueos`
--

INSERT INTO `parqueos` (`idParqueo`, `parPiso`, `parNumeroEspacio`, `parTipoVehiculo`, `parEstadoEspacio`, `parHoraEntrada`, `parHoraSalida`, `parEstado`, `fkIdVehiculo`, `fkIdTarifa`) VALUES
(1, 1, 101, 'Carro', 'DISPONIBLE', '2025-06-21 10:00:00', '2025-06-21 11:00:00', 'ACTIVO', 1, 1),
(2, 2, 202, 'Moto', 'OCUPADO', '2025-06-21 09:00:00', NULL, 'INACTIVO', 2, 2),
(3, 1, 103, 'Carro', 'DISPONIBLE', '2025-06-21 08:00:00', '2025-06-21 11:00:00', 'ACTIVO', 3, 1),
(4, 3, 304, 'Moto', 'OCUPADO', '2025-06-21 07:00:00', NULL, 'INACTIVO', 4, 2),
(5, 2, 205, 'Carro', 'DISPONIBLE', '2025-06-21 06:00:00', '2025-06-21 11:00:00', 'ACTIVO', 5, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `idReserva` int(11) NOT NULL,
  `resFechaReserva` date NOT NULL,
  `resHoraInicio` datetime NOT NULL,
  `resHoraFin` datetime NOT NULL,
  `resEstado` enum('RESERVADO','CANCELADO','FINALIZADO') DEFAULT 'RESERVADO',
  `resPiso` int(11) DEFAULT NULL,
  `resNumeroEspacio` int(11) DEFAULT NULL,
  `fkIdParqueo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`idReserva`, `resFechaReserva`, `resHoraInicio`, `resHoraFin`, `resEstado`, `resPiso`, `resNumeroEspacio`, `fkIdParqueo`) VALUES
(1, '2025-06-20', '2025-06-21 08:00:00', '2025-06-21 10:00:00', 'RESERVADO', 1, 101, 1),
(2, '2025-06-19', '2025-06-21 09:00:00', '2025-06-21 11:00:00', 'CANCELADO', 2, 202, 2),
(3, '2025-06-18', '2025-06-21 10:00:00', '2025-06-21 12:00:00', 'FINALIZADO', 1, 103, 3),
(4, '2025-06-17', '2025-06-21 11:00:00', '2025-06-21 13:00:00', 'RESERVADO', 3, 304, 4),
(5, '2025-06-16', '2025-06-21 12:00:00', '2025-06-21 14:00:00', 'FINALIZADO', 2, 205, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `idRol` int(11) NOT NULL,
  `rolTipoRol` varchar(100) NOT NULL,
  `rolDescripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`idRol`, `rolTipoRol`, `rolDescripcion`) VALUES
(1, 'ADMINISTRADOR', 'Acceso total al sistema'),
(2, 'CLIENTE', 'Usuario que reserva y paga parqueaderos'),
(3, 'PORTERO', 'Control de accesos en el parqueadero');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifas`
--

CREATE TABLE `tarifas` (
  `idTarifa` int(11) NOT NULL,
  `tarTipoEspacio` varchar(50) DEFAULT NULL,
  `tarValorHora` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `tarifas`
--

INSERT INTO `tarifas` (`idTarifa`, `tarTipoEspacio`, `tarValorHora`) VALUES
(1, 'Carro', 2500.00),
(2, 'Moto', 1000.00);

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
  `usuClaveHash` varchar(255) DEFAULT NULL,
  `usuFechaRegistro` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `fkIdRol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuario`, `usuDocumento`, `usuNombreCompleto`, `usuCorreo`, `usuTelefono`, `usuClaveHash`, `usuFechaRegistro`, `fkIdRol`) VALUES
(1, '100000001', 'Juan Pérez', 'juanp@ejemplo.com', '3001234567', 'abc123', '2024-06-16 05:00:00', 1),
(2, '100000002', 'Ana Gómez', 'anag@ejemplo.com', '3102345678', 'abc123', '2024-06-17 05:00:00', 2),
(3, '100000003', 'Carlos Ruiz', 'carlosr@ejemplo.com', '3203456789', 'abc123', '2024-06-18 05:00:00', 2),
(4, '100000004', 'Luisa Martínez', 'luisa.m@ejemplo.com', '3009876543', 'abc123', '2024-06-19 05:00:00', 3),
(5, '100000005', 'Jorge Ramírez', 'jorger@ejemplo.com', '3108765432', 'abc123', '2024-06-20 05:00:00', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE `vehiculos` (
  `idVehiculo` int(11) NOT NULL,
  `vehPlaca` varchar(50) NOT NULL,
  `vehTipo` varchar(50) DEFAULT NULL,
  `vehColor` varchar(50) DEFAULT NULL,
  `vehMarca` varchar(50) DEFAULT NULL,
  `vehModelo` varchar(50) DEFAULT NULL,
  `fkIdUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `vehiculos`
--

INSERT INTO `vehiculos` (`idVehiculo`, `vehPlaca`, `vehTipo`, `vehColor`, `vehMarca`, `vehModelo`, `fkIdUsuario`) VALUES
(1, 'ABC123', 'Carro', 'Rojo', 'Chevrolet', 'Sail', 1),
(2, 'XYZ789', 'Moto', 'Negro', 'Yamaha', 'FZ', 2),
(3, 'LMN456', 'Carro', 'Blanco', 'Renault', 'Logan', 3),
(4, 'QWE234', 'Moto', 'Gris', 'Honda', 'CB190', 4),
(5, 'ZXC098', 'Carro', 'Azul', 'Mazda', '3', 5);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `descuentos`
--
ALTER TABLE `descuentos`
  ADD PRIMARY KEY (`idDescuento`);

--
-- Indices de la tabla `descuentos_aplicados`
--
ALTER TABLE `descuentos_aplicados`
  ADD PRIMARY KEY (`idDescuentoAplicado`),
  ADD KEY `fkIdPago` (`fkIdPago`),
  ADD KEY `fkIdDescuento` (`fkIdDescuento`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`idPago`),
  ADD KEY `fkIdParqueo` (`fkIdParqueo`);

--
-- Indices de la tabla `parqueos`
--
ALTER TABLE `parqueos`
  ADD PRIMARY KEY (`idParqueo`),
  ADD KEY `fkIdVehiculo` (`fkIdVehiculo`),
  ADD KEY `fkIdTarifa` (`fkIdTarifa`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`idReserva`),
  ADD KEY `fkIdParqueo` (`fkIdParqueo`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  ADD PRIMARY KEY (`idTarifa`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `usuDocumento` (`usuDocumento`),
  ADD KEY `fkIdRol` (`fkIdRol`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`idVehiculo`),
  ADD UNIQUE KEY `vehPlaca` (`vehPlaca`),
  ADD KEY `fkIdUsuario` (`fkIdUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `descuentos`
--
ALTER TABLE `descuentos`
  MODIFY `idDescuento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `descuentos_aplicados`
--
ALTER TABLE `descuentos_aplicados`
  MODIFY `idDescuentoAplicado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `idPago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `parqueos`
--
ALTER TABLE `parqueos`
  MODIFY `idParqueo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `idReserva` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `idRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  MODIFY `idTarifa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  MODIFY `idVehiculo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `descuentos_aplicados`
--
ALTER TABLE `descuentos_aplicados`
  ADD CONSTRAINT `descuentos_aplicados_ibfk_1` FOREIGN KEY (`fkIdPago`) REFERENCES `pagos` (`idPago`),
  ADD CONSTRAINT `descuentos_aplicados_ibfk_2` FOREIGN KEY (`fkIdDescuento`) REFERENCES `descuentos` (`idDescuento`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`fkIdParqueo`) REFERENCES `parqueos` (`idParqueo`);

--
-- Filtros para la tabla `parqueos`
--
ALTER TABLE `parqueos`
  ADD CONSTRAINT `parqueos_ibfk_1` FOREIGN KEY (`fkIdVehiculo`) REFERENCES `vehiculos` (`idVehiculo`),
  ADD CONSTRAINT `parqueos_ibfk_2` FOREIGN KEY (`fkIdTarifa`) REFERENCES `tarifas` (`idTarifa`);

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`fkIdParqueo`) REFERENCES `parqueos` (`idParqueo`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`fkIdRol`) REFERENCES `roles` (`idRol`);

--
-- Filtros para la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD CONSTRAINT `vehiculos_ibfk_1` FOREIGN KEY (`fkIdUsuario`) REFERENCES `usuarios` (`idUsuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
