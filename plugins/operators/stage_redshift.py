from airflow.hooks.S3_hook import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    """
    Copies JSON-formatted event or song data from S3 into Redshift staging tables.
    Supports:
      - Song data using JSON 'auto'
      - Log data using an explicit JSONPaths file

    Parameters:
        redshift_conn_id   (str): Airflow connection ID for Redshift
        aws_credentials_id (str): Airflow connection ID for AWS credentials
        table              (str): Target staging table in Redshift
        s3_bucket          (str): S3 bucket name
        s3_key             (str): S3 key/prefix
        jsonpaths_file     (str): Optional S3 path to JSONPaths file (for log_data)
        region             (str): AWS region (default: us-east-1)
    """

    ui_color = "#358140"

    @apply_defaults
    def __init__(
        self,
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="",
        s3_bucket="",
        s3_key="",
        jsonpaths_file=None,
        region="us-east-1",
        *args,
        **kwargs
    ):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.jsonpaths_file = jsonpaths_file
        self.region = region

    def execute(self, context):
        self.log.info(f"Staging data into Redshift table '{self.table}'")

        # Resolve AWS credentials from Airflow connection
        s3_hook = S3Hook(aws_conn_id=self.aws_credentials_id)
        credentials = s3_hook.get_credentials()
        access_key = credentials.access_key
        secret_key = credentials.secret_key

        # Build S3 path
        execution_date = context.get("execution_date")
        rendered_key = self.s3_key.format(execution_date=execution_date)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        self.log.info(f"S3 source path resolved to: {s3_path}")

        # Select JSON handling method
        if self.jsonpaths_file:
            json_option = f"FORMAT AS JSON 's3://{self.s3_bucket}/{self.jsonpaths_file}'"
            self.log.info(f"Using JSONPaths file: {self.jsonpaths_file}")
        else:
            json_option = "FORMAT AS JSON 'auto'"
            self.log.info("Using Redshift auto JSON parsing for song data")

        # Build Redshift COPY command
        copy_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{access_key}'
            SECRET_ACCESS_KEY '{secret_key}'
            REGION '{self.region}'
            {json_option}
            TIMEFORMAT AS 'epochmillisecs'
            TRUNCATECOLUMNS
            BLANKSASNULL
            EMPTYASNULL;
        """

        self.log.info("Final COPY command:")
        self.log.info(copy_sql)

        # Load data
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        redshift.run(copy_sql)

        self.log.info(f"Staging for table '{self.table}' completed.")

