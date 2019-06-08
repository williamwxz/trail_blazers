from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CountDataframeOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):

        super(CountDataframeOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id=redshift_conn_id
        self.tables=tables
        

    def execute(self, context):
        for param in self.tables:
            self.log.info("parameters: {}".format(param))
            self.count_dataframe(param[0])
        
        
    def count_dataframe(self, table):
        if len(table)==0:
            raise ValueError("Invalid parameters")
            
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Data quality check failed. {table} returned no results")
        