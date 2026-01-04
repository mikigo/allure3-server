# Allure3 Server

一个使用FastAPI构建的简单服务器，用于生成和提供Allure 3报告，兼容Allure 3的新架构和特性。

## 功能

- 上传测试结果（包含Allure 3结果的ZIP文件）
- 生成带有自定义路径和执行器信息的Allure 3报告
- 列出所有生成的报告
- 将生成的报告作为静态文件提供

## 安装

1. 克隆或下载此仓库

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 安装Allure 3（使用npm）：
   
   ```bash
   npm install -g allure
   ```
   
   注意：确保你的系统上已安装Node.js。

## 使用

1. 启动服务器：
   ```bash
   allure3-server start
   ```

2. 打开浏览器并导航到 `http://localhost:8000/docs` 访问Web界面


## API

### 上传测试结果
参考 `test/upload_results.py`

示例请求（Python）：
```python
import requests
import pathlib

url = "http://10.0.20.202:8000/api/result"
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
```

示例响应：
```json
{
    "fileName": "allure-results.zip",
    "uuid": "1037f8be-68fb-4756-98b6-779637aa4670"
}
```

### 生成报告
参考 `test/generate_report.py`

示例请求（Python）：
```python
import requests

url = "http://10.0.20.202:8000/api/report"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, data='{"uuid":"87b5ae6e-3e3e-4937-9509-54bd0ff12623"}')
result = resp.json()
print(result)
```

示例响应：
```json
{
    "uuid": "c994654d-6d6a-433c-b8e3-90c77d0e8163",
    "path": "master/666",
    "url": "http://localhost:8000/reports/87b5ae6e-3e3e-4937-9509-54bd0ff12623/",
 
}
```

