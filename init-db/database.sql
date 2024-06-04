-- Create database
CREATE SCHEMA IF NOT EXISTS restaurants_database;

-- Create restaurants table
CREATE TABLE IF NOT EXISTS restaurants_database.restaurants
(
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    contact_number VARCHAR(255) NOT NULL,
    rating DECIMAL(2, 1) DEFAULT NULL
);

-- Create reviews table
CREATE TABLE IF NOT EXISTS restaurants_database.reviews
(
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    restaurant_id BIGINT NOT NULL,
    username VARCHAR(255) NOT NULL,
    review TEXT NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants_database.restaurants (id)
)

-- Function to generate random restaurants names and addresses
CREATE OR REPLACE FUNCTION generate_random_string(length INTEGER DEFAULT 20)
RETURNS VARCHAR(length) AS $$
SELECT floor(random() * (26^length))::text || repeat('a', length);
$$ LANGUAGE plpgsql VOLATILE COST 100;
$$
