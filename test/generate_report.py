import requests

url = "http://10.0.20.202:8000/api/report"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, data='{"uuid":"35f9f55b-6dd5-4bad-9bae-9a11fb335091"}')
result = resp.json()
print(result)