Tasks:
1. [Use the data source above, please create a Star schema of the Origin Sakila Database.](#use-the-data-source-above-please-create-a-star-schema-of-the-origin-sakila-database)

2. [From the star schema that you created in no 1, please create an airflow DAG that transforms data from Origin Sakila Schema to your new Star Schema that runs daily.](#from-the-star-schema-that-you-created-in-no-1-please-create-an-airflow-dag-that-transforms-data-from-origin-sakila-schema-to-your-new-star-schema-that-runs-daily)

3. [Please create a step by step comment of your dags in your python scripts and why you choose a certain approach from table creation to table insertion.](#from-the-star-schema-that-you-created-in-no-1-please-create-an-airflow-dag-that-transforms-data-from-origin-sakila-schema-to-your-new-star-schema-that-runs-daily)

4. [Create sample queries that demonstrate the difference between origin schema vs star schema for the same output.](#create-sample-queries-that-demonstrate-the-difference-between-origin-schema-vs-star-schema-for-the-same-output)

5. [Create the Data Warehouse Architecture.](#create-the-data-warehouse-architecture)

6. [Create Data Visualization based on the created Star Schema.](#create-data-visualization-based-on-the-created-star-schema)

# Answer

## Use the data source above, please create a Star schema of the Origin Sakila Database.

![Alt text](images/erd.jpg?raw=true "Title")

## From the star schema that you created in no 1, please create an airflow DAG that transforms data from Origin Sakila Schema to your new Star Schema that runs daily.

[airflow code](airflow/)

## Please create a step by step comment of your dags in your python scripts and why you choose a certain approach from table creation to table insertion.

The explanation of the Airflow's DAGs are explained in the DAGs itself and also here [Airflow README.md](airflow/README.md)

##  Create sample queries that demonstrate the difference between origin schema vs star schema for the same output.

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

2. __Average Rental Duration for Each Film Category__

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

## Create the Data Warehouse Architecture

![Alt text](images/pipeline.jpg?raw=true "Title")

This data pipeline starts with Debezium as the Change Data Capture mechanism to capture real-time changes from source databases like MySQL and Postgres, and streaming them to Google Cloud Pub/Sub. 

A Python subscriber service then consumes these changes and inserts the raw data to the data lake (BigQuery). It follows the ELT approach where unprocessed data is stored on a single place and will be transformed after.

Apache Airflow will be used to integrate data from additional sources. The data is stored within a BigQuery data warehouse. So the data from OLTP (MySQL, Postgres, etc) can be easily joined with data from third party APIs within BigQuery.

Apache Airflow also will be used to create the dim/fact tables to support analytics need.

The visualization or reporting tool will use Metabase, as it has a good integration with BigQuery.

## Create Data Visualization based on the created Star Schema

The code to generate the visualization is here [create_visualization.py](create_visualization.py)
1. Weekly Rental Trends
    
   Number of rentals aggregated weekly
   ![Alt text](images/rental_trends.jpeg?raw=true "Title")

2. Top 10 Cities by Customer Count
    ![Alt text](images/top_city.jpg?raw=true "Title")

3. Sales by Staff
    
    (Apparently dataset only has 2 staff)
    ![Alt text](images/sales_by_staff.jpg?raw=true "Title")