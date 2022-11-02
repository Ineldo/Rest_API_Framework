import requests

headers={'Authorization': 'Bearer bfdf24a74f18644093dbd03e933706aaec9154b3'}

endpoint ="http://localhost:8000/api/articles/"
data={
    "title":"Let's do this",
    "body":"I have created a new article today"
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())
