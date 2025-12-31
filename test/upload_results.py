import requests
import pathlib

url = "http://127.0.0.1:8000/api/result"
zipfile_path = "./allure-results.zip"
filename = pathlib.Path(zipfile_path).name
headers = {"accept": "*/*"}
with open(zipfile_path, "rb") as file:
   files = {
      "allure_results": (filename, file, "application/x-zip-compressed"),
   }
   resp = requests.post(url, files=files, headers=headers)
   result = resp.json()
   print(result)