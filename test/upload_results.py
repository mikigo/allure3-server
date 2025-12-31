import requests

url = "http://10.0.20.202:8000/api/result"
files = {
   "allureResults": open("allure-results.zip", "rb")
}
response = requests.post(url, files=files)
result = response.json()
result_uuid = result["uuid"]