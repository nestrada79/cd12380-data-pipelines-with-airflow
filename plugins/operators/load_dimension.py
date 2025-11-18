from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 table="",
                 sql_statement="",
                 insert_mode="truncate",   # options: "truncate" or "append"
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_statement = sql_statement
        self.insert_mode = insert_mode.lower()

    def execute(self, context):
        self.log.info(f"Starting dimension load for table: {self.table}")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Truncate mode (delete → insert)
        if self.insert_mode == "truncate":
            self.log.info(f"Truncating dimension table {self.table} before insert")
            redshift.run(f"DELETE FROM {self.table}")

        # Build final insert SQL
        insert_sql = f"""
            INSERT INTO {self.table}
            {self.sql_statement};
        """

        self.log.info(f"Loading data into dimension table {self.table}")
        redshift.run(insert_sql)

        self.log.info(f"Dimension table {self.table} loaded successfully.")

