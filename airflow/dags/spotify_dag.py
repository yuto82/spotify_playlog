from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
import sys

sys.path.append('/opt/airflow/src')

from pipeline.extract import extract
from pipeline.transform import transform
from pipeline.load import load

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2025, 6, 27),
    'retries': 2,
    'retry_delay': timedelta(minutes=60),
}

with DAG(
    dag_id='spotify_playlog',
    default_args=default_args,
    description='Pipeline to retrieve recently played tracks from Spotify.',
    schedule_interval='0 16 * * *',
    catchup=False,
    tags=['spotify_playlog']

) as dag:
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load
    )

    extract_task >> transform_task >> load_task