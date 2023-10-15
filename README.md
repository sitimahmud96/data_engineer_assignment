#  Create sample queries that demonstrate the difference between origin schema vs star schema for the same output.

Let's say we need to find out:
1. __Total sales for each film category.__

    Origin Schema:
    ```sql
    SELECT 
        YEAR(r.rental_date), 
        c.name AS category_name, 
        SUM(p.amount) AS total_sales
    FROM 
        category c
    JOIN 
        film_category fc ON c.category_id = fc.category_id
    JOIN 
        film f ON fc.film_id = f.film_id
    JOIN 
        inventory i ON f.film_id = i.film_id
    JOIN 
        rental r ON i.inventory_id = r.inventory_id
    JOIN 
        payment p ON r.rental_id = p.rental_id
    GROUP BY 
        1, c.name
    order by 
        total_sales desc;

    ```

    Star Schema:
    ```sql
    SELECT 
        YEAR(sf.rental_date) , 
        fd.category, 
        SUM(sf.payment_amount) AS total_sales
    FROM 
        fact_sales sf
    JOIN 
        dim_film fd ON sf.film_key = fd.film_key
    GROUP BY 
        YEAR(sf.rental_date), fd.category
    order by 
        total_sales desc;
    ```

    With the origin schema there are 7 tables that need to be joined, and the analyst also has to understand the relationship for each of the tables. On star schema the analyst can easily do the same thing with only 2 tables which make it easier and should also improve the query performance.

2. Average Rental Duration for Each Film Category

    Origin Schema:
    ```sql
    SELECT
        cat.name AS category_name,
        AVG(TIMESTAMPDIFF(DAY, rental_date, return_date)) AS avg_duration
    FROM
        rental r
    JOIN 
        inventory i ON r.inventory_id = i.inventory_id
    JOIN 
        film f ON i.film_id = f.film_id
    JOIN
        film_category fc ON f.film_id = fc.film_id
    JOIN
        category cat ON fc.category_id = cat.category_id
    GROUP BY
        cat.name
    ORDER BY
        avg_duration DESC;
    ```

    Star Schema:
    ```sql
    SELECT
        df.category AS category_name,
        AVG(frd.duration) AS avg_duration
    FROM
        fact_rental_duration frd
    JOIN 
        dim_film df ON frd.film_key = df.film_key
    GROUP BY
        df.category
    ORDER BY
        avg_duration DESC;

    ```
    With the star schema the query is more straightforward so the analyst can focus to generate insights.

# Create the Data Warehouse Architecture

![Alt text](images/pipeline.JPG?raw=true "Title")

This data pipeline starts with Debezium as the Change Data Capture mechanism to capture real-time changes from source databases like MySQL and Postgres (C), and streaming them to Google Cloud Pub/Sub. 

A Python subscriber service then consumes these changes and inserts the raw data to the data lake (BigQuery). It follows the ELT approach where unprocessed data is stored on a single place and will be transformed after.

Apache Airflow will be used to integrate data from additional sources. The data is stored within a BigQuery data warehouse. So the data from OLTP (MySQL, Postgres, etc) can be easily joined with data from third party APIs within BigQuery.

Apache Airflow also will be used to create the dim/fact tables to support analytics need.

The visualization or reporting tool will use Metabase, as it has a good integration with BigQuery.