from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import re


class DataQualityOperator(BaseOperator):
    ui_color = "#89DA59"

    @apply_defaults
    def __init__(
        self,
        redshift_conn_id="",
        tests=None,
        *args,
        **kwargs,
    ):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tests = tests or []

    def execute(self, context):
        self.log.info("Running Data Quality checks...")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if not self.tests:
            raise ValueError("No data quality tests provided.")

        for idx, test in enumerate(self.tests, start=1):
            sql = test.get("sql")
            expected = test.get("expected")

            if not sql or expected is None:
                raise ValueError(f"Test #{idx} is missing 'sql' or 'expected' fields")

            self.log.info(f"Running test #{idx}: {sql}")

            records = redshift.get_records(sql)

            if not records or not records[0]:
                raise ValueError(f"Test #{idx} returned no results: {sql}")

            actual = records[0][0]
            self.log.info(f"Test #{idx} returned value: {actual}")

            # Evaluate expected condition
            if isinstance(expected, str) and re.match(r"^(>=|<=|>|<|==|!=)\s*\d+$", expected):
                # Parse operator and value
                op, value = re.findall(r"(>=|<=|>|<|==|!=)|(\d+)", expected)
                op = [o for o in op if o][0]  # Operator from match
                value = int([v for v in value if v][0])

                comparison_str = f"{actual} {op} {value}"
                if not eval(comparison_str):
                    raise ValueError(
                        f"Data quality test #{idx} failed: Expected {expected} but got {actual}"
                    )

            # Expected exact numeric value
            elif isinstance(expected, int):
                if actual != expected:
                    raise ValueError(
                        f"Data quality test #{idx} failed: Expected {expected}, got {actual}"
                    )

            else:
                raise ValueError(
                    f"Invalid expected value for test #{idx}: {expected}. "
                    f"Use an integer or comparison string like '>0', '>=5', '==0'."
                )

            self.log.info(f"Test #{idx} passed successfully.")

        self.log.info("All Data Quality checks passed.")
