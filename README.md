# Machine Learning and Operations

## Overview

This repository contains a collection of hands-on projects developed as part of the **Machine Learning and Operations (MLOps)** coursework. The projects explore the complete machine learning lifecycle, including data versioning, experiment tracking, feature engineering, workflow orchestration, model deployment, containerization, CI/CD automation, and monitoring.

The objective is to understand how machine learning models can be developed, managed, deployed, automated, and monitored using industry-standard tools and technologies.

The repository consists of eight assignments, each focusing on a different component of the MLOps ecosystem.

---

## Assignments

### Assignment 1 – Data Version Control (DVC)

**Focus:** Dataset and ML pipeline versioning.

Topics covered:
- Introduction to Data Version Control.
- Dataset tracking and version management.
- Reproducibility of machine learning experiments.
- Managing datasets independently of source code.
- Versioning machine learning pipeline artifacts.

**Technology:** Python, DVC, Git.

### Assignment 2 – MLflow Experiment Tracking

**Focus:** Managing and tracking machine learning experiments.

Topics covered:
- MLflow Tracking.
- Experiment and run management.
- Logging model parameters and performance metrics.
- Model artifact storage.
- Comparing multiple machine learning experiments.
- Reproducibility and experiment organization.

**Technology:** Python, MLflow, Pandas, Scikit-learn.

### Assignment 3 – Feature Engineering Pipeline

**Focus:** Building a structured machine learning preprocessing pipeline.

Topics covered:
- Data loading and exploration.
- Data cleaning and preprocessing.
- Handling missing values.
- Feature transformation and encoding.
- Feature engineering.
- Building reusable preprocessing workflows.
- Preparing datasets for machine learning models.

**Technology:** Python, Pandas, NumPy, Scikit-learn.

### Assignment 4 – Workflow Automation Using Apache Airflow

**Focus:** Automating and orchestrating data pipelines.

The project demonstrates an automated student attendance data pipeline consisting of:

1. Data Extraction
2. Data Validation
3. Data Processing
4. Report Generation
5. Notification

Topics covered:
- Directed Acyclic Graphs (DAGs).
- Task dependencies and execution order.
- Scheduled workflow execution.
- Manual DAG triggering.
- Task monitoring and execution logs.
- Automated data processing.

**Technology:** Apache Airflow, Python, Pandas, Docker, Docker Compose.

### Assignment 5 – Machine Learning Model Deployment Using FastAPI

**Focus:** Exposing a trained