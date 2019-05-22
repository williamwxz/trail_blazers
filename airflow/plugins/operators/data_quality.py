from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 primary_keys=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.tables=tables
        self.primary_keys=primary_keys
        

    def execute(self, context):
        for param in zip(self.tables, self.primary_keys):
            self.log.info("parameters: {}".format(param))
            self.check_null(param[0], param[1])
        
        
    def check_null(self, table, primary_key):
        if len(table)==0 or len(primary_key)==0:
            raise ValueError("Invalid parameters")
            
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        records = redshift.get_records(f"SELECT COUNT(*) FROM {table} where {primary_key}=NULL")
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Data quality check failed. {table} returned no results")
        num_records = records[0][0]
        if num_records > 0:
            raise ValueError(f"Data quality check failed. {table} contained {num_records} null primary key")
        self.log.info(f"Data quality on table {table} check passed with {records[0][0]} null records")    
        
            
            
        
        