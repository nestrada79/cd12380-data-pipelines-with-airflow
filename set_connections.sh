#!/bin/bash
echo "Re-adding Airflow connections using environment variables..."

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
  echo "❌ AWS environment variables not found! Check your .env or Docker Compose."
  exit 1
else
  echo "✅ AWS credentials detected."
fi

if [ -z "$REDSHIFT_PASSWORD" ]; then
  echo "❌ Redshift password not found! Check your .env file."
  exit 1
else
  echo "✅ Redshift password detected."
fi

airflow connections add 'aws_credentials' \
    --conn-type 'aws' \
    --conn-login "${AWS_ACCESS_KEY_ID}" \
    --conn-password "${AWS_SECRET_ACCESS_KEY}"

airflow connections add 'redshift' \
    --conn-type 'postgres' \
    --conn-host 'default-workgroup.937211224345.us-east-1.redshift-serverless.amazonaws.com' \
    --conn-schema 'dev' \
    --conn-login 'awsuser' \
    --conn-password "${REDSHIFT_PASSWORD}" \
    --conn-port '5439'

