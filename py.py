import requests

url = "http://127.0.0.1:5000/recommend"
data = {
    "start": "MG Road",
    "destination": "Indiranagar",
    "traffic": "Jam on MG Road",
    "weather": "Rainy"
}

response = requests.post(url, json=data)
print(response.json())
