from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
# from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
#                                 LoadDimensionOperator, DataQualityOperator)
# from airflow.operators import LoadFactOperator
from helpers import SqlQueries
from airflow.models import Variable

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')
HOST = "redshift"

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

dag = DAG('project5',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          catchup=False
        )

# start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# stage_events_to_redshift = StageToRedshiftOperator(
#     create_tables_sql="/home/workspace/airflow/create_tables.sql",
#     redshift_conn_id=HOST,
#     table="staging_events",
#     s3_bucket="dend/log_data",
#     region="us-west-2",
#     task_id='Stage_events',
#     dag=dag
# )

# stage_songs_to_redshift = StageToRedshiftOperator(
#     create_tables_sql="/home/workspace/airflow/create_tables.sql",
#     redshift_conn_id=HOST,
#     table="staging_songs",
#     s3_bucket="dend/song_data",
#     region="us-west-2",
#     task_id='Stage_songs',
#     dag=dag
# )

# load_songplays_table = LoadFactOperator(
#     sql_command=SqlQueries.songplay_table_insert,
#     redshift_conn_id=HOST,
#     task_id='Load_songplays_fact_table',
#     dag=dag
# )

# load_user_dimension_table = LoadDimensionOperator(
#     sql_command=SqlQueries.user_table_insert,
#     redshift_conn_id=HOST,
#     task_id='Load_user_dim_table',
#     dag=dag
# )

# load_song_dimension_table = LoadDimensionOperator(
#     sql_command=SqlQueries.song_table_insert,
#     redshift_conn_id=HOST,
#     task_id='Load_song_dim_table',
#     dag=dag
# )

# load_artist_dimension_table = LoadDimensionOperator(
#     sql_command=SqlQueries.artist_table_insert,
#     redshift_conn_id=HOST,
#     task_id='Load_artist_dim_table',
#     dag=dag
# )

# load_time_dimension_table = LoadDimensionOperator(
#     sql_command=SqlQueries.time_table_insert,
#     redshift_conn_id=HOST,
#     task_id='Load_time_dim_table',
#     dag=dag
# )

# run_quality_checks = DataQualityOperator(
#     redshift_conn_id=HOST,
#     tables=['users', 'songs', 'artists','time'],
#     primary_keys=['userid','songid', 'artistid', 'start_time'],
#     task_id='Run_data_quality_checks',
#     dag=dag
# )

# end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# start_operator>>stage_events_to_redshift
# start_operator>>stage_songs_to_redshift

# stage_events_to_redshift>>load_songplays_table
# stage_songs_to_redshift>>load_songplays_table

# load_songplays_table>>load_user_dimension_table
# load_songplays_table>>load_song_dimension_table
# load_songplays_table>>load_artist_dimension_table
# load_songplays_table>>load_time_dimension_table

# load_user_dimension_table>>run_quality_checks
# load_song_dimension_table>>run_quality_checks
# load_artist_dimension_table>>run_quality_checks
# load_time_dimension_table>>run_quality_checks

# run_quality_checks>>end_operator


