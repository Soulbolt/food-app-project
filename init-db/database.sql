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

-- Function to generate random phone numbers
CREATE OR REPLACE FUNCTION generate_phone_number()
RETURNS VARCHAR(20) AS $$
DECLARE
  phone_number VARCHAR(20);
BEGIN
  phone_number := '(' || floor(random() * 900) + 100 || ') ';
  phone_number := phone_number || floor(random() * 9000) + 1000 || '-';
  phone_number := phone_number || floor(random() * 9000) + 1000;
  RETURN phone_number;
END;
$$ LANGUAGE plpgsql VOLATILE COST 100;
$$

-- Function to generate random ratings
CREATE OR REPLACE FUNCTION generate_random_rating()
RETURNS DECIMAL(2, 1) AS $$
BEGIN
  RETURN floor(random() * (50 - 30) + 30) / 10.0;
END;
$$ LANGUAGE plpgsql VOLATILE COST 100;
$$

-- Function to generate random number of reviews for a restaurant (1-5)
CREATE OR REPLACE FUNCTION generate_random_number_reviews_count()
RETURNS DECIMAL(2, 1) AS $$
BEGIN
  RETURN floor(random() * (5 - 1) + 1);
END;
$$ LANGUAGE plpgsql VOLATILE COST 100;
$$

-- Insert 100 random restaurants data into restaurants table
BEGIN;
  FOR i IN 1..100 LOOP
    INSERT INTO restaurants_database.restaurants (name, address, contact_number, rating)
    VALUES
    (
      generate_random_string(),
      generate_random_string(50),
      generate_phone_number(),
      generate_random_rating()
    );

    -- Insert random number of reviews for each restaurant
    INSERT INTO restaurants_database.reviews (restaurant_id, username, review, rating)
    SELECT currval('restaurant_id_seq'), generate_random_string(), generate_random_string(100), generate_random_rating()
    FROM generate_series(1, generate_random_number_reviews_count());
  END LOOP;
  COMMIT;
  $$;

  DROP FUNCTION generate_random_string, generate_phone_number, generate_random_rating, generate_random_number_reviews_count;
