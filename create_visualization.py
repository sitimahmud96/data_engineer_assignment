import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_data(query):
    config = {
        "host": "127.0.0.1",
        "port": 3308,
        "user": "sakila",
        "password": "p_ssW0rd",
        "database": "sakila"
    }
    conn = mysql.connector.connect(**config)

    df = pd.read_sql(query, conn)
    conn.close()
    return df

def plot_weekly_rental_trends():
    query = """
    SELECT rental_date, COUNT(*) AS num_rentals
    FROM fact_rental_duration
    GROUP BY rental_date;
    """

    df = get_data(query)
    df['rental_week_start'] = pd.to_datetime(df['rental_date']) - pd.to_timedelta(pd.to_datetime(df['rental_date']).dt.dayofweek, unit='D')
    df = df.groupby('rental_week_start').sum().reset_index()
    df = df.query('rental_week_start != "2006-02-13"')

    plt.figure(figsize=(10, 4)) 
    sns.lineplot(data=df, x='rental_week_start', y='num_rentals', marker='o')
    
    plt.xticks(df['rental_week_start'], rotation=45)
    
    plt.title('Weekly Rental Trends')
    plt.xlabel('Week Starting Date')
    plt.ylabel('Number of Rentals')
    plt.tight_layout()
    plt.savefig('rental_trends.jpg', format='jpg', dpi=300)
    plt.close()

def plot_customer_distribution():
    query = """
    SELECT city, country, COUNT(customer_key) AS num_customers
    FROM dim_customer
    GROUP BY city, country
    ORDER BY num_customers DESC
    LIMIT 10;  -- Limiting to top 10 cities for better visualization
    """

    df = get_data(query)
    
    df['city_country'] = df['city'] + ', ' + df['country']

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='city_country', y='num_customers', palette='viridis')
    
    plt.title('Top 10 Cities by Customer Count')
    plt.xlabel('City, Country')
    plt.ylabel('Number of Customers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_city.jpg', format='jpg', dpi=300)
    plt.close()

def plot_sales_by_staff():
    query = """
    SELECT ds.first_name, ds.last_name, SUM(frs.payment_amount) AS total_sales
    FROM fact_sales frs
    JOIN dim_staff ds ON frs.staff_key = ds.staff_key
    GROUP BY ds.first_name, ds.last_name
    ORDER BY total_sales DESC;
    """

    df = get_data(query)
    
    df['staff_name'] = df['first_name'] + ' ' + df['last_name']

    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x='staff_name', y='total_sales', palette='viridis')
    
    plt.title('Total Sales by Staff')
    plt.xlabel('Staff Name')
    plt.ylabel('Total Sales Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sales_by_staff.jpg', format='jpg', dpi=300)
    plt.close()

if __name__ == "__main__":
    
    plot_weekly_rental_trends()
    plot_customer_distribution()
    plot_sales_by_staff()