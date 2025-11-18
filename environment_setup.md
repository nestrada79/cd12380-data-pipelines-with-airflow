## 🧮 Environment Variable Setup & Instructions

This project uses a `.env` file for securely loading AWS and Redshift credentials into Docker containers.

### 1️⃣ Create `.env` in Project Root
Create a file named `.env` alongside `docker-compose.yaml`:
```bash
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
REDSHIFT_PASSWORD=YOUR_REDSHIFT_PASSWORD
AWS_DEFAULT_REGION=us-east-1
AIRFLOW_UID=50000
```
> ⚠️ `.env` is ignored by Git. Each developer or grader must create their own local version.

---

### 2️⃣ Docker Compose Integration
Both the scheduler and webserver services load environment variables automatically:
```yaml
env_file:
  - .env
environment:
  <<: *airflow-common-env
  AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
  AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
  REDSHIFT_PASSWORD: ${REDSHIFT_PASSWORD}
```

---

### 3️⃣ Verify Variables Inside Containers
To confirm Airflow sees your credentials:
```bash
docker exec -it cd12380-data-pipelines-with-airflow-airflow-scheduler-1 bash
env | grep -E 'AWS|REDSHIFT'
```
Expected output:
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=/7adma6/...
REDSHIFT_PASSWORD=...
```

---

### 4️⃣ Run Connection Setup Script
Run this to register your connections in Airflow:
```bash
docker exec -it cd12380-data-pipelines-with-airflow-airflow-scheduler-1 bash /opt/airflow/set_connections.sh
```

Expected output:
```
✅ AWS credentials detected.
✅ Redshift password detected.
✅ Airflow connections added successfully.
```

---

### 5️⃣ Example `.env.example` (for sharing safely)
```bash
# Example Airflow environment variables
AWS_ACCESS_KEY_ID=your-access-key-here
AWS_SECRET_ACCESS_KEY=your-secret-key-here
REDSHIFT_PASSWORD=your-redshift-password-here
AWS_DEFAULT_REGION=us-east-1
AIRFLOW_UID=50000
```

---

Once this setup is complete, Airflow can securely connect to both AWS S3 and Redshift using environment variables instead of hardcoded credentials.


