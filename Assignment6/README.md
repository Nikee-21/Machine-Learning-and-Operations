# Assignment 6: Containerize ML Model Using Docker

## Aim
To containerize a trained Machine Learning model
using Docker and deploy it through a FastAPI application.

## Objective
- Understand Docker and containerization.
- Create a Dockerfile.
- Build a Docker image.
- Run an ML application inside a container.
- Access the deployed API through a browser.

## Technologies Used
- Python 3.12
- FastAPI
- Scikit-learn
- Docker
- Uvicorn
- Joblib

## Machine Learning Model
Iris Classification using Random Forest Classifier.

## Docker Implementation

1. Install Docker Desktop.
2. Create a Dockerfile.
3. Build the Docker image.
4. Run the Docker container.
5. Access the FastAPI application.

## Docker Commands

Check Docker:
docker --version

Build image:
docker build -t iris-ml .

List images:
docker images

Run container:
docker run -d -p 8000:8000 --name iris-container iris-ml

List running containers:
docker ps

View logs:
docker logs iris-container

Stop container:
docker stop iris-container

Remove container:
docker rm iris-container

Remove image:
docker rmi iris-ml

## API Documentation

http://localhost:8000/docs

## Expected Outcome

The Iris classification model runs inside a Docker
container and provides predictions through a REST API.