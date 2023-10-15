TRUNCATE dim_store;

INSERT INTO dim_store (store_key, address, city, country, manager_first_name, manager_last_name)
SELECT s.store_id,
       a.address,
       ci.city,
       co.country,
       st.first_name,
       st.last_name
FROM store s
JOIN address a ON s.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id
JOIN staff st ON s.manager_staff_id = st.staff_id;
