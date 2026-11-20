import time
import requests

URL = "http://localhost:8000/predict"
VALID_PAYLOAD = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}
INVALID_PAYLOAD = {
    "sepal_length": -1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
}


def send_requests(count=50, delay=0.2):
    for index in range(count):
        payload = INVALID_PAYLOAD if index % 10 == 0 else VALID_PAYLOAD
        try:
            response = requests.post(URL, json=payload, timeout=5)
            print(index + 1, response.status_code, response.text)
        except requests.RequestException as exc:
            print("Request failed:", exc)
        time.sleep(delay)


if __name__ == "__main__":
    send_requests()
