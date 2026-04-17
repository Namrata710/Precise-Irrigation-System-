import requests
import random
import time

while True:
    data = {
        "soil_moisture": random.randint(10, 60)
    }
    response = requests.post("http://127.0.0.1:5000/predict", json=data)
    print(response.json())
    time.sleep(5)
