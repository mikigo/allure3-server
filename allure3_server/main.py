import os
import pathlib
import shutil
import subprocess
import uuid
import zipfile
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from allure3_server.__version__ import __version__ as version
from allure3_server.config import config


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
    uuid: str


class Allure3Server:

    def __init__(
            self,
            *,
            results_dir: str = None,
            reports_dir: str = None,
            host_ip: str = None,
            port: int = None,
            config_file: int = None,
    ):

        self.results_dir = results_dir or config.RESULTS_DIR
        os.makedirs(self.results_dir, exist_ok=True)
        self.reports_dir = reports_dir or config.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)

        self.host_ip = host_ip or config.HOST_IP
        self.port = port or config.PORT
        self.config_file = config_file or config.CONFIG_FILE

        self.app = FastAPI(
            title="Allure3 Server",
            description="A simple server for generating and serving Allure reports",
            version=str(version),
            docs_url=None,
            redoc_url=None
        )
        self.setup_routes()

    def _mount_static_files(self, app: FastAPI):
        app.mount(
            "/reports",
            StaticFiles(
                directory=pathlib.Path(self.reports_dir).resolve(),
                html=True
            ),
            name="reports"
        )
        app.mount(
            "/static",
            StaticFiles(
                directory=pathlib.Path(config.STATIC_DIR).resolve(),
                follow_symlink=True,
                check_dir=True,
            ),
            name="static"
        )

        @app.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url="/static/swagger-ui-bundle.js",
                swagger_css_url="/static/swagger-ui.css",
                swagger_favicon_url="/static/favicon.png",
            )

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()

    def setup_routes(self):
        app = self.app

        @app.get("/")
        async def root():
            return RedirectResponse(url="/docs")

        @app.post("/api/result")
        async def upload_results(allure_results: UploadFile = File(...)):
            return await self.upload_results(allure_results)

        @app.post("/api/report")
        async def generate_report(request: GenerateReportRequest = Body(...)):
            return await self.generate_report(request)

        @app.get("/api/reports")
        async def list_reports():
            return await self.list_reports()

        @app.delete("/api/reports/{report_id}")
        async def delete_report(report_id: str):
            return await self.delete_report(report_id)

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
                members = zip_ref.namelist()

                if members:
                    from os.path import commonprefix
                    common_prefix = commonprefix(members)

                    if common_prefix and (common_prefix.endswith('/') or common_prefix.endswith('\\')):
                        for member in zip_ref.infolist():
                            if member.filename.startswith(common_prefix):
                                member.filename = member.filename[len(common_prefix):]

                            if member.filename:
                                zip_ref.extract(member, result_path)
                    else:
                        zip_ref.extractall(result_path)
            os.remove(zip_file_path)

            return {"file_name": allure_results.filename, "uuid": uuid_str}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading results: {str(e)}")

    async def generate_report(self, request: GenerateReportRequest = Body(...)):
        try:
            result_path = os.path.join(self.results_dir, request.uuid)
            if not pathlib.Path(result_path).exists():
                raise HTTPException(status_code=404, detail=f"Allure results not found: {request.uuid}")
            report_path = os.path.join(self.reports_dir, request.uuid)
            os.makedirs(report_path, exist_ok=True)
            generate_cmd = ["npx"]
            generate_cmd.extend([
                "allure",
                "generate",
                result_path,
                "-o",
                report_path,
                "--config",
                self.config_file,
            ])
            proc = subprocess.run(generate_cmd,
                                  capture_output=True,
                                  shell=False,
                                  check=True,
                                  text=True)
            print(proc.stdout)
            print(proc.stderr)

            return {
                "uuid": request.uuid,
                "url": f"http://{self.host_ip}:{self.port}/reports/{request.uuid}/",
            }
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

    async def list_reports(self, ):
        try:
            reports = []
            for report_id in os.listdir(self.reports_dir):
                report_path = os.path.join(self.reports_dir, report_id)
                if os.path.isdir(report_path):
                    created_at = os.path.getctime(report_path)
                    reports.append({
                        "report_id": report_id,
                        "created_at": created_at,
                        "report_url": f"/reports/{report_id}"
                    })
            reports.sort(key=lambda x: x["created_at"], reverse=True)
            return {"reports": reports}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listing reports: {str(e)}")

    # 删除报告
    async def delete_report(self, report_id: str):
        try:
            report_path = os.path.join(self.reports_dir, report_id)
            if not os.path.exists(report_path):
                raise HTTPException(status_code=404, detail="Report not found")
            shutil.rmtree(report_path)
            return {"message": "Report deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")

    # 配置静态文件服务

    def start(self):
        self._mount_static_files(self.app)
        uvicorn.run(self.app, host=self.host_ip, port=self.port)
