from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = "#358140"

    template_fields = ("s3_key",)

    copy_sql = """
        COPY {table}
        FROM '{s3_path}'
        ACCESS_KEY_ID '{access_key}'
        SECRET_ACCESS_KEY '{secret_key}'
        FORMAT AS JSON '{json_path}'
        REGION 'us-east-1';
    """

    @apply_defaults
    def __init__(
        self,
        table="",
        s3_bucket="",
        s3_key="",
        json_path="auto",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        *args,
        **kwargs,
    ):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context):

        self.log.info(f"Starting COPY into Redshift table: {self.table}")

        # Get AWS credentials from Airflow connection
        aws_hook = S3Hook(aws_conn_id=self.aws_credentials_id)
        credentials = aws_hook.get_credentials()

        # Build full S3 path
        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        self.log.info(f"Loading data from {s3_path}")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Clear table before load (Udacity requirement)
        self.log.info(f"Clearing data from Redshift table {self.table}")
        redshift.run(f"DELETE FROM {self.table}")

        # Build COPY command
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            table=self.table,
            s3_path=s3_path,
            json_path=self.json_path,
            access_key=credentials.access_key,
            secret_key=credentials.secret_key,
        )

        self.log.info("Running COPY command...")
        redshift.run(formatted_sql)

        self.log.info(f"Successfully loaded data into {self.table}")
