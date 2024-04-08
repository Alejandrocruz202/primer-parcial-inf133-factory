import requests

url = "http://localhost:8000/orders"


headers = {"Content-Type": "application/json"}

data = {"orden_type": "fisico",
        "client": "Juan Perez",
        "payment": "Tarjeta de credito",
        "shipping": 10,
        "products":["camiseta","pantalon","zapatos"]        
        }
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print("Error scheduling delivery:", response.text)
