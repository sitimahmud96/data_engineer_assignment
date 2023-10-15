CREATE TABLE IF NOT EXISTS fact_sales (
    sales_fact_id INT AUTO_INCREMENT PRIMARY KEY,
    rental_date DATE,
    customer_key INT,
    film_key INT,
    staff_key INT,
    store_key INT,
    rental_id INT,
    payment_amount DECIMAL(5,2),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (film_key) REFERENCES dim_film(film_key),
    FOREIGN KEY (staff_key) REFERENCES dim_staff(staff_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);