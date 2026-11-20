# Student Placement Prediction using CI/CD

## 1. Project Overview

This project implements a Machine Learning pipeline to predict whether a student is likely to get placed based on academic performance and other relevant factors.

The project integrates **Continuous Integration (CI)** and **Continuous Deployment (CD)** using GitHub Actions to automate model training, testing, validation, and deployment checks.

## 2. Objectives

- Build a Machine Learning model for student placement prediction.
- Validate the dataset before training.
- Automate model training and testing.
- Verify that model accuracy is at least 80%.
- Implement a CI/CD workflow using GitHub Actions.
- Automate deployment checks after successful testing.

## 3. Dataset Description

The dataset contains student information with the following attributes:

| Attribute | Description |
|---|---|
| CGPA | Student's academic performance |
| Attendance | Attendance percentage |
| CodingScore | Coding assessment score |
| Projects | Number of completed projects |
| Internship | Internship status (0 or 1) |
| Placement | Placement result (0 or 1) |

The `Placement` column is the target variable.

## 4. Technologies Used

- Python
- Pandas
- Scikit-learn
- Joblib
- Pytest
- Git and GitHub
- GitHub Actions

## 5. Project Structure

```text
Assignment7/
│
├── data/
│   └── student_placement.csv
│
├── artifacts/
│   ├── model.pkl
│   └── accuracy.txt
│
├── train.py
├── predict.py
├── test_model.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── .github/
    └── workflows/
        └── ml-ci-cd.yml
```

The `artifacts/` folder is generated during model training and is excluded from Git.

## 6. Model Development

A Decision Tree Classifier is used to predict student placement.

The training process includes:

1. Loading the student placement dataset.
2. Checking required columns and missing values.
3. Validating placement labels.
4. Separating input features and target variable.
5. Splitting the dataset into training and testing sets.
6. Training the Decision Tree model.
7. Evaluating model accuracy.
8. Saving the trained model using Joblib.

The trained model is saved as `artifacts/model.pkl`, and its accuracy is stored in `artifacts/accuracy.txt`.

## 7. Prediction

The `predict.py` file loads the trained model and predicts the placement outcome for a sample student.

The output indicates whether the student is:

- PLACED
- NOT PLACED

## 8. Automated Testing

The `test_model.py` file contains automated tests to verify:

- Whether the trained model exists.
- Whether the accuracy file exists.
- Whether model accuracy is at least 80%.
- Whether prediction functionality works.
- Whether prediction outputs valid placement labels.

Pytest is used to execute these tests.

## 9. CI/CD Pipeline

GitHub Actions is used to automate the workflow whenever code is pushed to the `main` branch or a pull request is created.

### Continuous Integration (CI)

The CI process performs the following operations:

1. Checks out the latest repository code.
2. Sets up the Python environment.
3. Installs project dependencies.
4. Executes model training.
5. Runs automated tests.
6. Checks the model accuracy threshold.
7. Executes the prediction script.

### Continuous Deployment (CD)

The deployment job runs only after the CI job succeeds.

It performs a demonstration deployment check and confirms that the model has passed the quality checks.

**Note:** This assignment demonstrates the deployment stage through GitHub Actions. It does not deploy the model to an external hosting platform.

## 10. Expected Outcome

The project demonstrates how Machine Learning workflows can be automated using CI/CD practices.

It reduces manual intervention, improves testing consistency, and ensures that model quality checks are performed before the deployment stage.