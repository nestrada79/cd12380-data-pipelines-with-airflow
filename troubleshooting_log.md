# Troubleshooting Guide  
CD12380 / WGU D608  
Airflow • Docker • Redshift • S3  
**Author:** Natasha Estrada  
**Last Updated:** 2025-11-17

This document captures all major issues encountered during the setup and debugging of the Udacity CD12380 Data Pipelines project, along with root causes and exact resolutions.

---

# 1. Environment and Docker Issues

## 1.1 Airflow command not recognized on host
**Symptom:**
```
airflow : The term 'airflow' is not recognized
```

**Cause:** Airflow is inside Docker, not installed on Windows.

**Fix:**
```bash
docker exec -it cd12380-data-pipelines-with-airflow-airflow-webserver-1 bash
```

---

## 1.2 Airflow UI log viewer returning 403 errors
**Symptom:**
```
Signature verification failed
403 FORBIDDEN
```

**Cause:** Worker, scheduler, triggerer, and webserver had mismatched `secret_key`.

**Fix:**
```bash
docker-compose down -v
docker-compose up --build
```

---

## 1.3 DAG code not updating in worker
**Cause:** Celery worker cached plugin files.

**Fix:**
```bash
docker-compose down
docker-compose up --force-recreate --build
```

---

## 1.4 Python prompt inside container shows blank cursor
**Cause:** Python REPL was running but no prompt rendered.

**Fix:** Press Enter, then exit with:
```python
exit()
```
or Ctrl+D.

---

# 2. AWS and Credential Issues

## 2.1 Two active IAM access keys caused misalignment
**Symptom:** Redshift COPY returned:
```
InvalidAccessKeyId
```

**Cause:** Redshift was using an older key that Airflow no longer used.

**Fix:**
- Deleted the older key in IAM.
- Verified the correct one:
```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
S3Hook('aws_credentials').get_credentials().access_key
```

---

## 2.2 COPY command using deleted key
**Cause:** Old cached credentials inside Redshift and Airflow.

**Fix:**
- Rebuilt Docker containers
- Verified S3 connectivity

---

## 2.3 S3 prefix not found
**Symptom:**
```
The specified S3 prefix does not exist
```

**Cause:** COPY attempted exact file paths.

**Fix:** Verified keys inside container:
```python
hook.list_keys('airflow-project-nestr')
```

---

# 3. Redshift Schema and COPY Issues

## 3.1 staging_songs loaded zero rows
**Symptom:**
```
0 rows loaded
```
Airflow still marked the task as SUCCESS.

**Cause:** COPY failed silently. Airflow only checks Python return status, not Redshift result.

**Fix:** Query Redshift error tables:
```sql
SELECT * FROM pg_catalog.sys_load_error_detail ORDER BY start_time DESC;
```

---

## 3.2 Permission denied for STL tables
**Symptom:**
```
permission denied for stl_loaderror_detail
```

**Cause:** Redshift Serverless restricts classic STL tables.

**Fix:** Use supported views:
- `sys_load_error_detail`
- `stl_user_load_error_detail`

---

## 3.3 VARCHAR lengths too short
**Symptom:**
```
String length exceeds DDL length
```

**Cause:** Artist names and locations were longer than 256 characters.

**Fix:** Update schema:
```sql
artist_location VARCHAR(500),
artist_name     VARCHAR(500),
title           VARCHAR(500)
```

---

## 3.4 JSON 'auto' fails for the song dataset
**Cause:** Song data requires explicit JSONPath definitions.

**Fix:**
- Uploaded `song_json_path.json` to S3
- Updated COPY command:
```sql
JSON 's3://airflow-project-nestr/song_json_path.json'
```

---

## 3.5 Manual COPY succeeded with JSONPath
**Result:**  
Redshift successfully loaded:
```
385,252 records
```

---

## 3.6 DAG re-triggers truncate the table
**Cause:** StageToRedshiftOperator uses:
```sql
DELETE FROM {table}
```

**Resolution:**  
Confirmed this is expected Udacity behavior.

---

# 4. Airflow Operator Issues and Solutions

## 4.1 Deprecated import warnings
**Fix:**
```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
```

---

## 4.2 JSONPath parameter missing in DAG file
**Fix:**
```python
json_path="s3://airflow-project-nestr/song_json_path.json"
```

---

## 4.3 Airflow worker using old plugin code
**Fix:** Full container rebuild:
```bash
docker-compose down
docker-compose up --build
```

---

# 5. Commands Used for Verification

## 5.1 Check S3 from inside Airflow
```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
hook = S3Hook('aws_credentials')
hook.list_keys(bucket_name='airflow-project-nestr')
```

## 5.2 Manual Redshift COPY
```sql
COPY staging_songs
FROM 's3://airflow-project-nestr/song-data/'
CREDENTIALS 'aws_access_key_id=XXX;aws_secret_access_key=YYY'
JSON 's3://airflow-project-nestr/song_json_path.json'
REGION 'us-east-1';
```

## 5.3 Redshift load error inspection
```sql
SELECT *
FROM pg_catalog.sys_load_error_detail
ORDER BY start_time DESC;
```

---

# 6. Final Status

- All Airflow containers running correctly  
- S3 connectivity validated  
- Redshift IAM credentials aligned  
- staging_events table loads successfully  
- staging_songs loads **385,252 rows**  
- Operator logic fully functional  
- Test DAGs pass  
- Git repository updated and clean  

---

# 7. Lessons Learned

- Redshift COPY failures do not automatically fail Airflow tasks  
- Redshift Serverless uses different system tables  
- Docker rebuild is often required after plugin changes  
- JSONPath is required for the song dataset  
- IAM consistency is critical for both Airflow and Redshift  

---


