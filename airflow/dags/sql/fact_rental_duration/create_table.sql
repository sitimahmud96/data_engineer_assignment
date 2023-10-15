CREATE TABLE IF NOT EXISTS fact_rental_duration (
    rental_key INT PRIMARY KEY AUTO_INCREMENT,  
    film_key INT,                               
    customer_Key INT,                           
    rental_date DATE,                           
    return_date DATE,                           
    duration INT
);
