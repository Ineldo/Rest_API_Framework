import requests


#endpoint ="https://httpbin.org/anything"
endpoint ="http://localhost:8000/api/"#"http://127.0.0.1:8000/

get_response = requests.post(endpoint, json={"content": "Hey you "})
#print(get_response.text)
#print(get_response.headers)

# print(get_response.json())
# print(get_response.status_code)
print(get_response.json())
