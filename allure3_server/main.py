import json
import os
import shutil
import subprocess
import uuid
import zipfile
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from allure3_server.config import config

app = FastAPI(title="Allure3 Server", description="A simple server for generating and serving Allure reports")


class ExecutorInfo(BaseModel):
    buildName: str
    buildUrl: str = None
    buildOrder: int = None
    reportUrl: str = None
    reportName: str = None


class ReportSpec(BaseModel):
    path: List[str]
    executorInfo: Optional[ExecutorInfo] = None


class GenerateReportRequest(BaseModel):
    uuid_str: str


class Allure3Server:

    def __init__(self, results_dir: str = None, reports_dir: str = None):

        self.results_dir = results_dir or config.RESULTS_DIR
        os.makedirs(self.results_dir, exist_ok=True)
        self.reports_dir = reports_dir or config.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)

    @app.get("/")
    async def root(self):
        return {"message": "Allure3 Server is running!"}

    @app.post("/api/result")
    async def upload_results(self, allure_results: UploadFile = File(...)):
        try:
            if not allure_results.filename.endswith('.zip'):
                raise HTTPException(status_code=400, detail="Only ZIP files are supported")

            uuid_str = str(uuid.uuid4())
            result_path = os.path.join(self.results_dir, uuid_str)
            os.makedirs(result_path, exist_ok=True)
            zip_file_path = os.path.join(result_path, allure_results.filename)

            with open(zip_file_path, "wb") as buffer:
                shutil.copyfileobj(allure_results.file, buffer)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(result_path)
            os.remove(zip_file_path)

            return {"fileName": allure_results.filename, "uuid": uuid_str}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading results: {str(e)}")

    @app.post("/api/report")
    async def generate_report(self, request: GenerateReportRequest = Body(...)):
        try:
            for result_id in request.results:
                result_path = os.path.join(self.results_dir, result_id)
                if not os.path.exists(result_path):
                    raise HTTPException(status_code=404, detail=f"Results with UUID {result_id} not found")
            uuid_str = str(uuid.uuid4())
            report_path = os.path.join(self.reports_dir, uuid_str)
            os.makedirs(report_path, exist_ok=True)
            generate_cmd = [
                "npx",
                "allure",
                "generate",
                self.results_dir,
                "-o",
                report_path
            ]

            subprocess.run(generate_cmd, shell=True, check=True)

            # 返回结果
            return {
                "uuid": uuid_str,
                "path": report_path,
                "url": f"http://localhost:8000/reports/{report_path}/",
            }
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

    # 列出所有报告
    @app.get("/api/reports")
    async def list_reports(self, ):
        try:
            reports = []
            for report_id in os.listdir(self.reports_dir):
                report_path = os.path.join(self.reports_dir, report_id)
                if os.path.isdir(report_path):
                    # 获取报告创建时间
                    created_at = os.path.getctime(report_path)
                    reports.append({
                        "report_id": report_id,
                        "created_at": created_at,
                        "report_url": f"/reports/{report_id}"
                    })

            # 按创建时间排序
            reports.sort(key=lambda x: x["created_at"], reverse=True)

            return {"reports": reports}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listing reports: {str(e)}")

    # 删除报告
    @app.delete("/api/reports/{report_id}")
    async def delete_report(self, report_id: str):
        try:
            report_path = os.path.join(self.reports_dir, report_id)

            # 检查报告是否存在
            if not os.path.exists(report_path):
                raise HTTPException(status_code=404, detail="Report not found")

            # 删除报告目录
            shutil.rmtree(report_path)

            return {"message": "Report deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")

    # 配置静态文件服务

    def start(self):
        import uvicorn
        app.mount("/reports", StaticFiles(directory=self.reports_dir, html=True), name="reports")
        uvicorn.run(app, host="0.0.0.0", port=8000)
