from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators import StageToRedshiftOperator, DataQualityOperator, CountDataframeOperator
from helpers import SqlQueries
from airflow.models import Variable

HOST = "redshift"

DEMOGRAPHICS_TABLE="demographics"
IMMIGRATION_TABLE="immigration"
AIRPORT_TABLE="airport"

BUCKET='us-immigration-data'

default_args = {
    'owner': 'wzhang',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    # 'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('capstone',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          catchup=False
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_demographics_to_redshift = StageToRedshiftOperator(
    redshift_conn_id=HOST,
    table=DEMOGRAPHICS_TABLE,
    s3_bucket=BUCKET+'/us-cities-demographics.csv',
    region="us-west-2",
    task_id='Stage_demographics',
    delimiter=';',
    dag=dag
)

stage_immigration_to_redshift = StageToRedshiftOperator(
    redshift_conn_id=HOST,
    table=IMMIGRATION_TABLE,
    s3_bucket=BUCKET+'/immigration_data_sample.csv',
    region="us-west-2",
    task_id='Stage_immigration',
    dag=dag
)

stage_airport_to_redshift = StageToRedshiftOperator(
    redshift_conn_id=HOST,
    table=AIRPORT_TABLE,
    s3_bucket=BUCKET+'/airport-codes_csv.csv',
    region="us-west-2",
    task_id='Stage_airport',
    dag=dag
)

run_null_checks = DataQualityOperator(
    redshift_conn_id=HOST,
    tables=[DEMOGRAPHICS_TABLE, IMMIGRATION_TABLE, AIRPORT_TABLE],
    primary_keys=['userid','songid', 'artistid', 'start_time'],
    task_id='Run_null_checks',
    dag=dag
)

run_count_checks = CountDataframeOperator(
    redshift_conn_id=HOST,
    tables=[DEMOGRAPHICS_TABLE, IMMIGRATION_TABLE, AIRPORT_TABLE],
    task_id='Run_count_checks',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator>>stage_demographics_to_redshift
start_operator>>stage_immigration_to_redshift
start_operator>>stage_airport_to_redshift

stage_demographics_to_redshift>>run_null_checks
stage_immigration_to_redshift>>run_null_checks
stage_airport_to_redshift>>run_null_checks

run_null_checks>>run_count_checks

run_count_checks>>end_operator
