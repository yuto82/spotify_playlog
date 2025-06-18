from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook    
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=60),

}
with DAG(
    'spotify_dag',
    default_args=default_args,
    schedule_interval='10 4 * * *',  # This DAG will run at 10 min past mindnight (12:10)EST, The rason I have build 4:10 because my airflow follows UTC timestamp
):

    exchange = PythonOperator(
        task_id = 'exchange_token',
        python_callable = exchange_token
    )

    refresh = PythonOperator(
        task_id = 'refresh_token',
        python_callable = refresh_token
    )

    get_songs = PythonOperator(
        task_id= 'get_songs',
        python_callable = get_recently_played_tracks
    )

# Dependancies 
exchange >> refresh >> get_songs