import requests

url = "http://localhost:8000/orders"


headers = {"Content-Type": "application/json"}
orden_type = "fisico"
data = {"orden_type": orden_type}
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print("Error scheduling delivery:", response.text)
