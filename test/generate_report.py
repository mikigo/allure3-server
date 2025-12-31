import requests

url = "http://127.0.0.1:8000/api/report"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, data='{"uuid":"d3b90916-2184-4800-beb7-0c002abe96d9"}')
result = resp.json()
print(result)