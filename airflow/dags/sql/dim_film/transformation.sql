TRUNCATE dim_film;

INSERT INTO dim_film (film_key, title, description, release_year, rental_duration, rental_rate, length, replacement_cost, rating, category)
SELECT f.film_id,
       f.title,
       f.description,
       f.release_year,
       f.rental_duration,
       f.rental_rate,
       f.length,
       f.replacement_cost,
       f.rating,
       c.name
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id;
