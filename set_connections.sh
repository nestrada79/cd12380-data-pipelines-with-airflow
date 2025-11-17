#!/bin/bash

echo "--------------------------------------------------"
echo "Re-adding Airflow connections using environment variables..."
echo "--------------------------------------------------"

# Validate AWS ENV VARS
if [[ -z "$AWS_ACCESS_KEY_ID" || -z "$AWS_SECRET_ACCESS_KEY" ]]; then
    echo "❌ AWS environment variables not found! Check your .env or docker-compose."
    exit 1
else
    echo "✅ AWS credentials detected."
fi

# Validate Redshift PW
if [[ -z "$REDSHIFT_PASSWORD" ]]; then
    echo "❌ Missing REDSHIFT_PASSWORD in .env"
    exit 1
else
    echo "✅ Redshift password detected."
fi

# Optional but recommended
if [[ -z "$AWS_DEFAULT_REGION" ]]; then
    echo "⚠️  AWS_DEFAULT_REGION not set — using us-east-1"
    AWS_DEFAULT_REGION="us-east-1"
else
    echo "🌎 AWS region: $AWS_DEFAULT_REGION"
fi

echo "🧹 Deleting old connections (if exist)..."
airflow connections delete aws_credentials > /dev/null 2>&1
airflow connections delete redshift > /dev/null 2>&1

echo "✨ Creating AWS connection..."
airflow connections add 'aws_credentials' \
    --conn-type 'aws' \
    --conn-login "$AWS_ACCESS_KEY_ID" \
    --conn-password "$AWS_SECRET_ACCESS_KEY" \
    --conn-extra "{\"region_name\": \"${AWS_DEFAULT_REGION}\"}"

echo "✨ Creating Redshift connection..."
airflow connections add 'redshift' \
    --conn-type 'postgres' \
    --conn-host 'default-workgroup.937211224345.us-east-1.redshift-serverless.amazonaws.com' \
    --conn-schema 'dev' \
    --conn-login 'awsuser' \
    --conn-password "${REDSHIFT_PASSWORD}" \
    --conn-port '5439'

echo "--------------------------------------------------"
echo "🎉 Airflow connections successfully configured!"
echo "--------------------------------------------------"
