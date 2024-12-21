from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
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
    host: str = Form(...),
    port: int = Form(...),
    scheme: str = Form(...),
    method: str = Form(...),
    path: str = Form(...),
    params: str = Form(...),
    headers: str = Form(...),
    expected_result: str = Form(...),
):
    # Генерация config.yaml
    config_data = {
        "config": {
            "host": host,
            "port": port,
            "scheme": scheme,
            "method": method,
            "path": path,
        },
        "get_params": yaml.safe_load(params) if params else {},
        "headers": yaml.safe_load(headers) if headers else {},
        "result": yaml.safe_load(expected_result),
    }

    config_path = "tests/config.yaml"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as file:
        yaml.dump(config_data, file)

    # Запуск теста
    try:
        result = subprocess.check_output(
            ["python", "YamlTester.py", "--config", config_path],
            # ["python", "YamlTester.py", "--yaml", json.dumps(config_data)],
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        result = e.output

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )
