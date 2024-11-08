import os
import sys

# чтобы работало из консоли
os.getcwd()
sys.path.append('PATH_TO_YOUR_SITE_PACKAGES')

import yaml
import requests
import argparse


class YamlParser:
    """Парсер для чтения конфигурации из YAML-файла."""
    def __init__(self, file_path):
        self.config = self._parse_yaml(file_path)

    def _parse_yaml(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)


class RequestBuilder:
    """Собирает параметры запроса из конфигурации."""
    def __init__(self, config):
        self.config = config['config']
        self.get_params = config.get('get_params', {})
        self.headers = config.get('headers', {})
        self.base_url = f"{self.config['scheme']}://{self.config['host']}:{self.config['port']}"
        self.path = self.config['path']
        self.method = self.config['method'].upper()

    def build_request(self):
        url = f"{self.base_url}{self.path}"
        request_data = {
            'method': self.method,
            'url': url,
            'params': self.get_params if self.method == 'GET' else None,
            'data': self.get_params if self.method == 'POST' else None,
            'headers': self.headers,
        }
        return request_data


class HttpClient:
    """Отправляет HTTP-запрос и возвращает ответ."""
    def send_request(self, request_data):
        method = request_data.pop('method')
        url = request_data.pop('url')

        if method == 'GET':
            response = requests.get(url, **request_data)
        elif method == 'POST':
            response = requests.post(url, **request_data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return response


class ResponseChecker:
    """Проверяет ответ на соответствие ожидаемому результату."""
    def __init__(self, expected_result):
        self.expected_result = expected_result

    def check_result(self, response):
        actual_result = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
        if actual_result == self.expected_result:
            print("Test passed!")
        else:
            print("Test failed!")
            print("Expected:", self.expected_result)
            print("Actual:", actual_result)


# Основной блок запуска
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YAML Test Client")
    parser.add_argument('--config', required=True, help="Path to the YAML configuration file")
    args = parser.parse_args()

    # Шаг 1: Чтение и парсинг конфигурации
    config = YamlParser(args.config).config

    # print(config.__class__)

    # Шаг 2: Сборка запроса
    request_builder = RequestBuilder(config)
    request_data = request_builder.build_request()

    # Шаг 3: Отправка запроса
    http_client = HttpClient()
    response = http_client.send_request(request_data)

    # Шаг 4: Проверка ответа
    checker = ResponseChecker(config['result'])
    checker.check_result(response)
