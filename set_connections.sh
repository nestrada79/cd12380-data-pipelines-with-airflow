#!/bin/bash

echo "Re-adding Airflow connections..."

airflow connections add 'aws_credentials' \
    --conn-type 'aws' \
    --conn-login 'YOUR_AWS_ACCESS_KEY' \
    --conn-password 'YOUR_AWS_SECRET_KEY'

airflow connections add 'redshift' \
    --conn-type 'postgres' \
    --conn-host 'default-workgroup.YOUR-ACCOUNT.us-east-1.redshift-serverless.amazonaws.com' \
    --conn-schema 'dev' \
    --conn-login 'awsuser' \
    --conn-password 'YOUR_REDSHIFT_PASSWORD' \
    --conn-port '5439'
