from typing import Optional

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import random
import string
import yaml
import subprocess

app = FastAPI()

# Подключение шаблонов и статических файлов
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Обработка формы
@app.post("/run-test", response_class=HTMLResponse)
async def run_test(
    request: Request,
    host: str = Form(None),
    port: Optional[int] = Form(None),
    scheme: str = Form(None),
    method: str = Form(None),
    path: str = Form(None),
    params: str = Form(None),
    headers: str = Form(None),
    expected_result: str = Form(None),
    config_file: UploadFile = File(None),
):
    # # Генерация config.yaml
    # config_data = {
    #     "config": {
    #         "host": host,
    #         "port": port,
    #         "scheme": scheme,
    #         "method": method,
    #         "path": path,
    #     },
    #     "get_params": yaml.safe_load(params) if params else {},
    #     "headers": yaml.safe_load(headers) if headers else {},
    #     "result": yaml.safe_load(expected_result),
    # }

    if config_file:
        config_data = yaml.safe_load(config_file.file)
        config_path = f"tests/{''.join(random.choices(string.ascii_uppercase + string.digits, k=7))}.yaml"
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(config_data, file)
    else:
        config_str = f'''
config:
    host: {host}
    port: {port if port else "~"}
    scheme: {scheme}
    method: {method}
    path: {path}
get_params: {yaml.safe_load(params) if params else ""}
headers: {yaml.safe_load(headers) if headers else ""}
result: {yaml.safe_load(expected_result)}
'''

    # Запуск теста
    try:
        if config_file:
            result = subprocess.check_output(
                ["python", "tester.py", "--config", config_path],
                stderr=subprocess.STDOUT,
                text=True
            )
        else:
            result = subprocess.check_output(
                ["python", "tester.py", "--yaml", config_str],
                stderr=subprocess.STDOUT,
                text=True
            )
    except subprocess.CalledProcessError as e:
        result = e.output

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )
