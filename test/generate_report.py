import requests

url = "http://10.0.20.202:8000/api/report"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, data='{"uuid":"87b5ae6e-3e3e-4937-9509-54bd0ff12623"}')
result = resp.json()
print(result)