from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 create_tables_sql="",
                 redshift_conn_id="",
                 table="",
                 s3_bucket="",
                 region="us-west-2",
                 delimiter=",",
                 ignore_headers=1,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.create_tables_sql=create_tables_sql
        self.redshift_conn_id=redshift_conn_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.region = region
        self.ignore_headers=ignore_headers
        self.delimiter=delimiter
        self.copy_command = """
                copy {}
                from '{}'
                iam_role 'arn:aws:iam::332608265013:role/UdacityRedshift'
                region '{}'
                ignoreheader {}
                delimiter '{}'
                csv;
            """


    def execute(self, context):
        self.log.info("staging table {}".format(self.table))
#         aws_hook = AwsHook(self.aws_credentials_id)
#         credentials = aws_hook.get_credentials()
        self.log.info("Getting connection to {}".format(self.redshift_conn_id))
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        rendered_key = ''
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        self.log.info("Copy from S3: {}".format(self.s3_bucket))
        command = self.copy_command.format(self.table, s3_path, self.region, self.ignore_headers, self.delimiter)
        self.log.info("Command: {}".format(command))
        
        redshift.run(command)
        return
    
    def create_tables(self, redshift):
        # Open and read the file as a single buffer
        self.log.info("run sql script {} to create tables".format(self.create_tables_sql))
        df = open(self.create_tables_sql, 'r')
        sqlScript=df.read()
        df.close()
        sqlCommands=sqlScript.split(';')
        for command in sqlCommands:
            self.log.info(command)
            command=command.strip()
            if len(command)==0:
                continue
            redshift.run(command)
        return
 
         
            
        