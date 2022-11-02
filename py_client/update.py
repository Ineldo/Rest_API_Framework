import requests

endpoint ="http://localhost:8000/api/products/14/update/"#"http://127.0.0.1:8000/

data ={
    "title": "Product done Updated",
    "price": 100001.99
}
get_response = requests.put(endpoint, json=data)

print(get_response.json())
