-- Create the database
CREATE DATABASE IF NOT EXISTS vulnerable_db;

-- Use db
USE vulnerable_db;

-- Create the users table
CREATE TABLE account (
id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    pass VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

INSERT INTO account (username, pass, email) VALUES ('admin', 'admin', 'admin@admin.com');
INSERT INTO account (username, pass, email) VALUES ('guest', 'guest', 'guest@guest.com');

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price VARCHAR(10) NOT NULL,
    color VARCHAR(20) NOT NULL
);

INSERT INTO products (name, price, color) VALUES ('apple', '2,50 EUR', 'red');
INSERT INTO products (name, price, color) VALUES ('watermelon', '8 EUR', 'green');
INSERT INTO products (name, price, color) VALUES ('banana', '2 EUR', 'yellow');

