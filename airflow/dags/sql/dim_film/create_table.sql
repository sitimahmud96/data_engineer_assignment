CREATE TABLE IF NOT EXISTS dim_film (
    film_key INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    release_year YEAR,
    rental_duration TINYINT,
    rental_rate DECIMAL(4,2),
    length SMALLINT,
    replacement_cost DECIMAL(5,2),
    rating ENUM('G','PG','PG-13','R','NC-17'),
    category VARCHAR(25)
);