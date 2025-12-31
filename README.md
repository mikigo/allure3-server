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
   python main.py
   ```

2. 打开浏览器并导航到 `http://localhost:8000` 访问Web界面

3. 或者，你可以直接使用API端点：

### API端点

#### 上传测试结果
- **POST** `/api/result`
- 表单数据：`allureResults`（包含Allure 3结果的ZIP文件）
- 响应：包含 `fileName` 和 `uuid` 的JSON

示例请求（Python）：
```python
import requests

url = "http://localhost:8080/api/result"
files = {
    "allureResults": open("allure-results.zip", "rb")
}
response = requests.post(url, files=files)
print(response.json())
```

示例响应：
```json
{
    "fileName": "allure-results.zip",
    "uuid": "1037f8be-68fb-4756-98b6-779637aa4670"
}
```

#### 生成报告
- **POST** `/api/report`
- 请求体：包含报告规格的JSON
- 响应：包含报告信息的JSON

示例请求（Python）：
```python
import requests
import json

url = "http://localhost:8080/api/report"
headers = {
    "Content-Type": "application/json"
}
payload = {
    "reportSpec": {
        "path": [
            "master",
            "666"
        ],
        "executorInfo": {
            "buildName": "#666"
        }
    },
    "results": [
        "1037f8be-68fb-4756-98b6-779637aa4670"
    ],
    "deleteResults": False
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json())
```

示例响应：
```json
{
    "uuid": "c994654d-6d6a-433c-b8e3-90c77d0e8163",
    "path": "master/666",
    "url": "http://localhost:8080/allure/reports/c994654d-6d6a-433c-b8e3-90c77d0e8163/",
    "latest": "http://localhost:8080/reports/master/666"
}
```

#### 列出报告
- **GET** `/api/reports`
- 响应：包含报告列表的JSON

示例请求（Python）：
```python
import requests

url = "http://localhost:8080/api/reports"
response = requests.get(url)
print(response.json())
```

#### 查看报告
- **GET** `/reports/{report_id}`
- **GET** `/allure/reports/{report_id}/`

## 示例工作流程

1. 上传测试结果：
   ```python
   import requests

   url = "http://localhost:8080/api/result"
   files = {
       "allureResults": open("allure-results.zip", "rb")
   }
   response = requests.post(url, files=files)
   result = response.json()
   result_uuid = result["uuid"]
   ```

2. 生成报告（使用上一步的UUID）：
   ```python
   import requests
   import json

   url = "http://localhost:8080/api/report"
   headers = {
       "Content-Type": "application/json"
   }
   payload = {
       "reportSpec": {
           "path": ["master", "666"],
           "executorInfo": {
               "buildName": "#666"
           }
       },
       "results": [result_uuid],
       "deleteResults": False
   }

   response = requests.post(url, headers=headers, data=json.dumps(payload))
   report_info = response.json()
   ```

3. 查看报告：在浏览器中打开响应中的 `url` 或 `latest` URL
