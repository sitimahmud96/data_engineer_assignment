CREATE TABLE IF NOT EXISTS dim_store (
    store_key INT PRIMARY KEY,
    address VARCHAR(255),
    city VARCHAR(50),
    country VARCHAR(50),
    manager_first_name VARCHAR(45),
    manager_last_name VARCHAR(45)
);
