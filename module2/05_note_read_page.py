import requests

response = requests.get("http://localhost:5173/")
print(response.status_code)
print(response.text)
