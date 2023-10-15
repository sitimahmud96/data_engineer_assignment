CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INT PRIMARY KEY,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    full_name VARCHAR(45),
    email VARCHAR(50),
    address VARCHAR(255),
    city VARCHAR(50),
    country VARCHAR(50)
);