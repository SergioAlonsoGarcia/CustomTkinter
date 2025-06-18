-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS `NOLOSE`;

-- Usar la base de datos NOLOSE
USE `NOLOSE`;

-- Crear la tabla `usuarios` si no existe
CREATE TABLE IF NOT EXISTS `usuarios` (
    `correo` VARCHAR(60) NOT NULL PRIMARY KEY,
    `usuario` VARCHAR(50) NOT NULL,
    `contraseña` VARCHAR(50) NOT NULL,
    `icono` VARCHAR (255)
);

-- Insertar los datos
INSERT INTO `usuarios`(`correo`,`usuario`,`contraseña`) VALUES('1','1','1','');