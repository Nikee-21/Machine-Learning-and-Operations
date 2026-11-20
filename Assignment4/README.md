# Assignment 4 – Build Workflow Automation Using Apache Airflow

## Objective
Build an automated, daily student-attendance data pipeline using Apache Airflow. The workflow performs:

1. Data Extraction
2. Data Validation
3. Data Processing
4. Report / Result Generation
5. Notification

The DAG is named `data_pipeline_dag`. It supports scheduled daily execution and manual triggering from the Airflow UI.

## Project structure

```text
Assignment4/
├── dags/
│   └── data_pipeline_dag.py
├── data/
│   └── student_attendance.csv
├── output/
├── logs/
├── plugins/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Pipeline behavior

- **Extraction:** Reads `data/student_attendance.csv` and writes an extracted copy.
- **Validation:** Checks required columns, empty data, missing values, duplicate student IDs, and valid attendance counts.
- **Processing:** Calculates attendance percentage and labels students as `Eligible` (>= 75%) or `Not Eligible` (< 75%).
- **Report generation:** Creates `output/summary_report.txt` with student counts and average attendance.
- **Notification:** Writes a completion message to `output/notification.txt` and the Airflow task log.

## Run with Docker Compose

Prerequisite: Docker Desktop with its Linux engine running.

From the Assignment4 directory:

```powershell
docker compose up --build -d
```

Open the Airflow UI at:

```text
http://localhost:8080
```

The official Airflow standalone image creates a local admin account on first startup. Retrieve the generated credentials from the container logs:

```powershell
docker compose logs airflow
```

Look for the generated username and password in the startup output. Keep credentials private.

In the Airflow UI:
1. Open `data_pipeline_dag`.
2. Confirm the DAG is unpaused.
3. Select **Trigger DAG** to run it manually.
4. Open the task graph and inspect task status and logs.

The DAG is also scheduled with `@daily`.

## Output files

After a successful run, these files appear in `output/`:

- `extracted_attendance.csv`
- `processed_attendance.csv`
- `summary_report.txt`
- `notification.txt`

Because `output/` is mounted from the host, generated results remain in this project folder.

## Stop the services

```powershell
docker compose down
```

To remove the container and its local Airflow metadata volume (if one is added later), use the appropriate Docker Compose volume cleanup only after confirming you no longer need that metadata.

## Notes

- This is a local demonstration pipeline. The notification task records a notification in a file and Airflow logs; it does not send an email or external alert.
- The sample CSV is included so the DAG has input data immediately.
- The code is prepared but has not been executed or tested in this package.
