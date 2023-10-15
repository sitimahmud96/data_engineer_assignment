import mysql.connector
import pandas as pd

def get_data():
    config = {
        "host": "127.0.0.1",
        "port": 3308,
        "user": "sakila",
        "password": "p_ssW0rd",
        "database": "sakila"
    }
    
    conn = mysql.connector.connect(**config)

    query = """SELECT
        df.category AS category_name,
        AVG(frd.duration) AS avg_duration
    FROM
        fact_rental_duration frd
    JOIN 
        dim_film df ON frd.film_key = df.film_key
    GROUP BY
        df.category
    ORDER BY
        avg_duration DESC;"""

    df = pd.read_sql(query, conn)
    
    conn.close()

    return df

if __name__ == "__main__":
    data = get_data()
    
    print('Average Rental Duration for Each Film Category')
    print(data.head())
