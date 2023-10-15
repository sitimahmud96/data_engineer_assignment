TRUNCATE dim_staff;


INSERT INTO dim_staff (staff_key, first_name, last_name, email, address, city, country)
SELECT st.staff_id,
       st.first_name,
       st.last_name,
       st.email,
       a.address,
       ci.city,
       co.country
FROM staff st
JOIN address a ON st.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
JOIN country co ON ci.country_id = co.country_id;
