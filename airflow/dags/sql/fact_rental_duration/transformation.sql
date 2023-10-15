TRUNCATE fact_rental_duration;
INSERT INTO fact_rental_duration (film_key, customer_Key, rental_date, return_date, duration)
SELECT
    f.film_key,
    c.customer_id,
    DATE(r.rental_date) AS rental_date,
    DATE(r.return_date) AS return_date,
    TIMESTAMPDIFF(DAY, r.rental_date, r.return_date) AS duration
FROM
    rental r
JOIN
    inventory i ON r.inventory_id = i.inventory_id
JOIN
    dim_film f ON i.film_id = f.film_key
JOIN
    customer c ON r.customer_id = c.customer_id;