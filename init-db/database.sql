CREATE SCHEMA IF NOT EXISTS restaurants_database;

CREATE TABLE IF NOT EXISTS restaurants_database.restaurants
(
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    contact_number VARCHAR(255) NOT NULL,
    rating DECIMAL(2, 1) DEFAULT NULL
);