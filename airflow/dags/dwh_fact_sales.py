import sqlalchemy as sa
import pandas as pd
import datetime
import numpy as np
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

DAG_ID = Path(os.path.basename(__file__)).stem # filename

# Default arguments
default_args = {
    'catchup': False,
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(DAG_ID, 
          schedule_interval='@daily',
          start_date=datetime(2023, 6, 19), 
          catchup=False,
          default_args=default_args) as dag:
    # from airflow.providers.postgres.hooks.postgres import PostgresHook
    # client_snaporder = PostgresHook('sb_snaporder').get_sqlalchemy_engine()	

    con = 'coba'

    t1 = DummyOperator(task_id="start")

    create_table = MySqlOperator(
        task_id="create_table",
        mysql_conn_id=con,
        sql='/sql/fact_sales/create_table.sql'
    )

    ingest_data = MySqlOperator(
        task_id="ingest_data",
        mysql_conn_id=con,
        sql='/sql/fact_sales/transformation.sql'
    )
    
    t3 = DummyOperator(task_id="end")    

    t1 >> create_table >> ingest_data >> t3