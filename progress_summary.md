## Udacity Project: Data Pipelines with Apache Airflow

**Project Type:** Data Engineering Nanodegree  
**Student:** Natasha Estrada  
**Last Updated:** 2025-11-07 02:25:15

---

## ✅ Project Setup Summary

### Project Directory
Working directory (Git-tracked):
```
C:\Users\nestr\cd12380-data-pipelines-with-airflow
```

### Project Structure
```
.
├── dags/                     # Contains final_project.py DAG and related code
├── plugins/                  # Custom operators (stage, fact, dimension, quality)
├── logs/                     # Airflow logs (auto-generated)
├── docker-compose.yaml       # Custom Airflow Docker setup
├── .env                      # AIRFLOW_UID=50000
├── README.md                 # Project instructions
├── create_tables.sql         # Redshift table creation SQL
├── airflow_home/             # (May contain Airflow local configs)
├── airflow1/                 # (Possibly unused or alternate setup)
```

---

## ✅ Environment Setup

- **Docker Desktop**: Running Airflow via `docker-compose`
- **Airflow Version**: `2.6.2`
- **Executor**: CeleryExecutor
- **UI Login**: `airflow / airflow`
- **Ports**: `localhost:8080`

### Docker Volumes
- DAGs mapped from: `./dags`
- Plugins mapped from: `./plugins`
- Logs stored in: `./logs`

---

## ✅ AWS Setup

- **AWS CLI Installed**: Confirmed with `aws sts get-caller-identity`
- **S3 Bucket Created**: `airflow-project-nestr`
- **Data Copied**:
  - Log data: `s3://airflow-project-nestr/log-data/`
  - Song data: `s3://airflow-project-nestr/song-data/`
  - Log JSON path file: `s3://airflow-project-nestr/log_json_path.json`

- **Configured Airflow connections for AWS and Redshift** Added test DAGs and troubleshoot

Data successfully verified with:
```bash
aws s3 ls s3://airflow-project-nestr/log-data/
aws s3 ls s3://airflow-project-nestr/song-data/
aws s3 ls s3://airflow-project-nestr/log_json_path.json
```

---

## 🔧 Next Steps

- [ ] Implement DAG operators (`StageToRedshift`, `LoadFact`, `LoadDimension`, `DataQuality`)
- [ ] Validate DAG dependency flow and logic
- [ ] Push completed project to GitHub and submit

---

## 📌 Notes

- Docker memory warning (under 4GB) acknowledged
- Example DAGs will be disabled in `docker-compose.yaml` for cleaner view
- This repo will contain all project code for grading and reproducibility
- Project being done locally on student’s computer d/t issues with Udacity workspace
- Used `set_connections.sh` to store AWS connections but added to `.gitignore` to keep credentials secret

---

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


