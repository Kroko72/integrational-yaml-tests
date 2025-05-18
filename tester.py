import sys
import logging

import site
from pathlib import Path


# Автоматическое определение пути к site-packages текущего окружения (чтобы работало из консоли)
def add_venv_site_packages():
    # 1. Проверка активированного виртуального окружения
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # 2. Используем системные пути через модуль site
        site_packages = site.getsitepackages()
        for path in site_packages:
            if 'site-packages' in path:
                sys.path.append(str(Path(path).resolve()))
                return

    # 3. Резервный вариант для нестандартных окружений
    venv_path = Path(sys.prefix) / "Lib" / "site-packages"
    if venv_path.exists():
        sys.path.append(str(venv_path.resolve()))


# Вызов функции
add_venv_site_packages()

from lib.config_parser import ConfigParser
from lib.request_builder import RequestBuilder
from lib.http_client import HttpClient
from lib.response_checker import ResponseChecker

import requests
import argparse

from typing import Dict, Any


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YAML/JSON Test Client')
    parser.add_argument('--config', help='Path to the YAML/JSON configuration file')
    parser.add_argument('--yaml', help='YAML configuration as a string')
    parser.add_argument('--json', help='JSON configuration as a string')
    args: argparse.Namespace = parser.parse_args()

    logger.setLevel(args.log_level)

    if not args.config and not args.yaml and not args.json:
        parser.error('Provide --config, --yaml, or --json.')

    # Шаг 1: Чтение конфигурации
    config: Dict[str, Any]
    if args.config:
        config = ConfigParser(file_path=args.config).config
    elif args.yaml:
        config = ConfigParser(yaml_string=args.yaml).config
    elif args.json:
        config = ConfigParser(json_string=args.json).config

    # Шаг 2: Сборка запроса
    request_builder: RequestBuilder = RequestBuilder(config=config)
    request_data: Dict[str, Any] = request_builder.build_request()

    # Шаг 3: Отправка запроса
    http_client = HttpClient(
        max_retries=config.get('retry', {}).get('max_retries', 3),
        retry_delay=config.get('retry', {}).get('retry_delay', 1),
        backoff_factor=config.get('retry', {}).get('backoff_factor', 2)
    )
    response: requests.Response = http_client.send_request(request_data)

    # Шаг 4: Проверка ответа
    checker: ResponseChecker = ResponseChecker(config['result'])
    checker.check_result(response)
