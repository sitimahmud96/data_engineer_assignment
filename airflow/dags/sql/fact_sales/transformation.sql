TRUNCATE fact_sales;
INSERT INTO fact_sales (rental_date, customer_key, film_key, staff_key, store_key, rental_id, payment_amount)
SELECT 
	date(r.rental_date) rental_date,
       cd.customer_key,
       fd.film_key,
       sd.staff_key,
       s.store_id,
       r.rental_id,
       p.amount
FROM rental r
JOIN payment p ON r.rental_id = p.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN dim_customer cd ON r.customer_id = cd.customer_key
JOIN dim_film fd ON f.film_id = fd.film_key
JOIN dim_staff sd ON r.staff_id = sd.staff_key
JOIN staff s ON r.staff_id = s.staff_id;