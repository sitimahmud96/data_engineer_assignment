## How to run the Airflow Pipeline
1. Assuming docker has been installed, run this command:

`docker compose -f docker-compose.yml -f docker-compose.local.yml up`

2. It will setup the containers, mainly there will be 3 containers that will run:
    - Airflow
    - Postgres as the Airflow metadata database
    - MySQL database that preloaded with `Sakila` example data (which exposed to the host as port 3308) [https://github.com/sakiladb/mysql](https://github.com/sakiladb/mysql)

    Tested on Windows

3. It might take ~5 minutes for the containers to be ready, visit [http://locahost:8080](http://localhost:8080) (user: airflow pass: airflow) for the Airflow Webserver. First turn on the dim tables and if it runs succesfuly turn on the fact tables.

![Alt text](../images/dims.jpg?raw=true "Title")

4. To query the results table of star schema, first do `pip install -r requirements.txt` it will install `mysql-connector-python and pandas` packages and then run `python run.py` which will output a query of __Average Rental Duration for Each Film Category__ based on the Sakila Star Schema that has been created.

![Alt text](../images/run_q.jpg?raw=true "Title")

## Date Warehouse Approach
The dim/fact tables run daily. The mechanism to create the DWH tables are TRUNCATE-INSERT, where it deletes existing data before inserts the data, this will be inefficient for large datasets. A more efficient alternative would be to use an UPDATE-INSERT strategy and only filter out the data before ingesting (usually based on `creation_date`), which can help reduce the processing workload.

## DAGs Structure
Each of the dim/fact tables have its own DAG. Mainly there are 2 tasks for the DAG:
- `create_table` responsible for creating the table based on corresponding schema.
- `ingest_data` responsible for transformation and insert data to table that have been created by `create_table` task.

It uses SQL templating to manage the SQLs so it will not cluttered the main DAG.

Example for `fact_sales`

`create_table.sql`
```sql
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_fact_id INT AUTO_INCREMENT PRIMARY KEY,
    rental_date DATE,
    customer_key INT,
    film_key INT,
    staff_key INT,
    store_key INT,
    rental_id INT,
    payment_amount DECIMAL(5,2)
);
```

`transformation.sql`
```sql
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
```