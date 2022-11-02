import requests

endpoint ="http://localhost:8000/api/products/5/"#"http://127.0.0.1:8000/

get_response = requests.get(endpoint, json={"content": "Hey you "})

print(get_response.json())
