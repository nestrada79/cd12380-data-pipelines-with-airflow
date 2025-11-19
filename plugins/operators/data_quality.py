from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    ui_color = "#89DA59"

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tests=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tests = tests

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for test in self.tests:
            sql = test["sql"]
            expected = test["expected"]

            records = redshift.get_records(sql)

            if len(records) == 0 or len(records[0]) == 0:
                raise ValueError(f"No results returned for query: {sql}")

            result = records[0][0]

            if result != expected:
                raise ValueError(
                    f"Data quality check failed. Query: {sql} "
                    f"Expected: {expected} Got: {result}"
                )

            self.log.info(f"Data quality check passed: {sql}")
