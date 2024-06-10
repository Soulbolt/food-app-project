-- Create a new schema
CREATE SCHEMA IF NOT EXISTS restaurant_schema;

-- Create the restaurants table
CREATE TABLE restaurant_schema.restaurants (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    rating DECIMAL(2, 1) NOT NULL,
    is_favorite BOOLEAN DEFAULT FALSE
);

-- Create the reviews table
CREATE TABLE restaurant_schema.reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurant_schema.restaurants(id) ON DELETE CASCADE,
    username VARCHAR(50) NOT NULL,
    review TEXT NOT NULL,
    rating INT NOT NULL
);

-- Function to generate random strings
-- CREATE OR REPLACE FUNCTION random_string(length INT) RETURNS TEXT AS $$
-- DECLARE
--     chars TEXT := 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
--     result TEXT := '';
--     i INT;
-- BEGIN
--     FOR i IN 1..length LOOP
--         result := result || substr(chars, floor(random() * length(chars) + 1)::int, 1);
--     END LOOP;
--     RETURN result;
-- END;
-- $$ LANGUAGE plpgsql;

-- Procedure to insert sample data
-- CREATE OR REPLACE PROCEDURE generate_sample_data()
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE
--     i INT;
--     j INT;
--     restaurant_id INT;
-- BEGIN
--     FOR i IN 1..100 LOOP
--         INSERT INTO restaurant_schema.restaurants (name, address, contact_number, rating)
--         VALUES (
--             'Restaurant ' || i,
--             random_string(10) || ' Street, Springfield, IL 6270' || (i % 10),
--             '(217) 555-' || lpad(i::text, 4, '0'),
--             round((random() * 4 + 1)::numeric, 1)
--         )
--         RETURNING id INTO restaurant_id;

--         -- Insert a few reviews for each restaurant
--         FOR j IN 1..(floor(random() * 5 + 1))::int LOOP
--             INSERT INTO restaurant_schema.reviews (restaurant_id, username, review, rating)
--             VALUES (
--                 restaurant_id,
--                 'user' || j,
--                 random_string(50),
--                 floor(random() * 5 + 1)::int
--             );
--         END LOOP;
--     END LOOP;
-- END;
-- $$;

-- Call the procedure to generate 100 random phone numbers
-- CALL generate_sample_data();

-- Query the tables to see the generated phone numbers
SELECT * FROM restaurant_schema.restaurants;
SELECT * FROM restaurant_schema.reviews;
