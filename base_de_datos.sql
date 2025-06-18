-- DROP DATABASE IF EXISTS `aplicacion`;

CREATE DATABASE IF NOT EXISTS `aplicacion`;

USE `aplicacion`;

-- Crear la tabla `usuarios` si no existe
CREATE TABLE IF NOT EXISTS `usuarios` (
    `correo` VARCHAR(60) NOT NULL PRIMARY KEY,
    `usuario` VARCHAR(50) NOT NULL,
    `contraseña` VARCHAR(50) NOT NULL,
    `icono` VARCHAR (255)
);
