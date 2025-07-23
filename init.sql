CREATE DATABASE IF NOT EXISTS fakenews;
USE fakenews;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    prediction VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* Insertar admin de prueba (opcional) */
/* Contraseña: admin123 (debes hashearla previamente si usas esto en producción) */
INSERT IGNORE INTO users (email, password, role) VALUES (
    'admin@admin.com',
    '$2b$12$U2qpAaLMOB8hJx2Z5zXJ.eZd5Gl6QFSQWlB54Z9yIEvNszugm7R3e',  -- hash de "admin123"
    'admin'
);
