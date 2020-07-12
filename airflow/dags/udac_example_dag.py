from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator,LoadFactOperator,
                               LoadDimensionOperator,DataQualityOperator)
from airflow.operators import PostgresOperator 
from helpers import SqlQueries
import datetime
from airflow.hooks.postgres_hook import PostgresHook

#AWS_KEY = os.environ.get('AWS_KEY')
#AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'Narayana-K',
    #'start_date' : datetime.datetime.now(),
    'start_date': datetime(2020, 7, 11),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup_by_default': False,
    'email_on_retry': False,
    'schedule_interval': '@hourly'
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)
create_tables_task = PostgresOperator(
        task_id="create_tables",
        dag=dag,
        sql='create_tables.sql',
        postgres_conn_id="redshift"
)
stage_usa_state_coviddata_to_redshift = StageToRedshiftOperator(
    task_id='Stage_usa_state_covid_data',
    dag=dag,
    provide_context=False,
    table = "staging_data_usa_states_covid19",
    s3_path = "s3://aws-deng-covid/enigma-nytimes-data-in-usa/us_states/part-00000-aa7e3dbc-cd43-4930-9596-fb0fd4167f5a-c000.json",
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    region="us-east-2",
    data_format="JSON"
)

stage_usa_county_coviddata_to_redshift = StageToRedshiftOperator(
    task_id='Stage_usa_county_covid_data',
    dag=dag,
    provide_context=False,
    table = "staging_data_usa_county_covid19",
    s3_path = "s3://aws-deng-covid/enigma-nytimes-data-in-usa/us_county/part-00000-3b0459c2-faeb-4548-a5f2-6107221e8871-c000.json",
    redshift_conn_id="redshift",
    aws_conn_id="aws_credentials",
    region="us-east-2",
    data_format="JSON"
)
load_covid_data_fact_table = LoadFactOperator(
    task_id='Load_covid_data_fact_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="usa_data_covid19",
    sql="usa_covid19_insert",
    append_only=False
)
Load_usa_state_dimension_table = LoadDimensionOperator(
    task_id='Load_usa_state_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="usa_state",
    sql="usa_state_table_insert",
    append_only=False
)
Load_usa_county_dimension_table = LoadDimensionOperator(
    task_id='Load_usa_county_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="usa_county",
    sql="usa_county_table_insert",
    append_only=False
)
load_date_dimension_table = LoadDimensionOperator(
    task_id='Load_date_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="date",
    sql="date_table_insert",
    append_only=False
)
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=["usa_data_covid19", "usa_state", "usa_county", "date"]
)
end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator>>create_tables_task
create_tables_task>>[stage_usa_state_coviddata_to_redshift ,stage_usa_county_coviddata_to_redshift]
[stage_usa_state_coviddata_to_redshift ,stage_usa_county_coviddata_to_redshift]>> load_covid_data_fact_table
load_covid_data_fact_table>>Load_usa_state_dimension_table>> run_quality_checks
load_covid_data_fact_table>>Load_usa_county_dimension_table>> run_quality_checks
load_covid_data_fact_table>>load_date_dimension_table>> run_quality_checks
run_quality_checks>>end_operator

