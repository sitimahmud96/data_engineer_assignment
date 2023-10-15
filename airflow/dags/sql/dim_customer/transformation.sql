TRUNCATE dim_customer;

INSERT INTO dim_customer (customer_key, first_name, last_name, full_name, email, address, city, country)
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       CONCAT(c.first_name, ' ', c.last_name) full_name,
       c.email,
       a.address,
       ci.city,
       co.country
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id;