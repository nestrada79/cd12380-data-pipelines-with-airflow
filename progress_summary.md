# Udacity Project: Data Pipelines with Apache Airflow

**Project Type:** Data Engineering Nanodegree  
**Student:** Andres Estrada  
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
- Project being done locally on students computer d/t issues with Udacity workspace

---
