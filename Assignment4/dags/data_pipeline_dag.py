from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import pendulum
from airflow.decorators import dag, task

DATA_DIR = Path("/opt/airflow/data")
OUTPUT_DIR = Path("/opt/airflow/output")
SOURCE_FILE = DATA_DIR / "student_attendance.csv"
EXTRACTED_FILE = OUTPUT_DIR / "extracted_attendance.csv"
PROCESSED_FILE = OUTPUT_DIR / "processed_attendance.csv"
REPORT_FILE = OUTPUT_DIR / "summary_report.txt"
NOTIFICATION_FILE = OUTPUT_DIR / "notification.txt"

REQUIRED_COLUMNS = {"student_id", "student_name", "total_classes", "attended_classes"}


@dag(
    dag_id="data_pipeline_dag",
    description="Daily student attendance data pipeline: extract, validate, process, report and notify.",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["assignment4", "data-pipeline", "mlops"],
)
def data_pipeline_dag():

    @task
    def data_extraction() -> str:
        """Load the source CSV and persist an extracted copy for the next task."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if not SOURCE_FILE.exists():
            raise FileNotFoundError(f"Input dataset not found: {SOURCE_FILE}")

        df = pd.read_csv(SOURCE_FILE)
        df.to_csv(EXTRACTED_FILE, index=False)
        logging.info("Extracted %s rows from %s", len(df), SOURCE_FILE.name)
        return str(EXTRACTED_FILE)

    @task
    def data_validation(extracted_path: str) -> str:
        """Validate schema, nulls, duplicate IDs and attendance ranges."""
        df = pd.read_csv(extracted_path)

        missing_columns = REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
        if df.empty:
            raise ValueError("Input dataset is empty.")
        if df[list(REQUIRED_COLUMNS)].isnull().any().any():
            raise ValueError("Required fields contain missing values.")
        if df["student_id"].duplicated().any():
            raise ValueError("Duplicate student_id values found.")
        if (df["total_classes"] <= 0).any():
            raise ValueError("total_classes must be greater than zero.")
        if (df["attended_classes"] < 0).any():
            raise ValueError("attended_classes cannot be negative.")
        if (df["attended_classes"] > df["total_classes"]).any():
            raise ValueError("attended_classes cannot exceed total_classes.")

        logging.info("Validation successful for %s records.", len(df))
        return extracted_path

    @task
    def data_processing(validated_path: str) -> str:
        """Calculate attendance percentage and minimum-attendance eligibility."""
        df = pd.read_csv(validated_path)
        df["attendance_percentage"] = (
            df["attended_classes"] / df["total_classes"] * 100
        ).round(2)
        df["eligibility"] = df["attendance_percentage"].apply(
            lambda value: "Eligible" if value >= 75 else "Not Eligible"
        )
        df.to_csv(PROCESSED_FILE, index=False)
        logging.info("Processed attendance data written to %s", PROCESSED_FILE)
        return str(PROCESSED_FILE)

    @task
    def report_generation(processed_path: str) -> str:
        """Generate a text summary report from the processed data."""
        df = pd.read_csv(processed_path)
        total_students = len(df)
        eligible = int((df["eligibility"] == "Eligible").sum())
        not_eligible = total_students - eligible
        average_attendance = float(df["attendance_percentage"].mean())

        report = (
            "STUDENT ATTENDANCE PIPELINE - SUMMARY REPORT\n"
            "============================================\n"
            f"Total students: {total_students}\n"
            f"Eligible (attendance >= 75%): {eligible}\n"
            f"Not eligible (attendance < 75%): {not_eligible}\n"
            f"Average attendance: {average_attendance:.2f}%\n"
            "\nGenerated automatically by Apache Airflow.\n"
        )
        REPORT_FILE.write_text(report, encoding="utf-8")
        logging.info("Summary report generated at %s", REPORT_FILE)
        return str(REPORT_FILE)

    @task
    def notification(report_path: str) -> None:
        """Record a completion notification after the report is generated."""
        message = (
            "SUCCESS: Student attendance data pipeline completed.\n"
            f"Report: {report_path}\n"
        )
        NOTIFICATION_FILE.write_text(message, encoding="utf-8")
        logging.info(message)

    extracted = data_extraction()
    validated = data_validation(extracted)
    processed = data_processing(validated)
    report = report_generation(processed)
    notification(report)


data_pipeline_dag()
