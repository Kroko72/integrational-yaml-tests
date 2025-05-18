import logging
from typing import Dict, Any


logger = logging.getLogger(__name__)


class RequestBuilder:
    """Собирает параметры запроса из конфигурации."""

    def __init__(self, config: Dict[str, Any]) -> None:
        logger.info("Building request parameters")
        self.config = config['config']
        self.retry_params = self.config.get('retry', {})
        self.get_params: Dict[str, Any] = config.get('get_params', {})
        self.headers: Dict[str, Any] = config.get('headers', {})

        if self.config['port'] is not None:
            self.base_url: str = f"{self.config['scheme']}://{self.config['host']}:{self.config['port']}"
        else:
            self.base_url: str = f"{self.config['scheme']}://{self.config['host']}"

        self.path: str = self.config['path']
        self.method: str = self.config['method'].upper()

    def build_request(self) -> Dict[str, Any]:
        url = f"{self.base_url}{self.path}"
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Method: {self.method}, Headers: {self.headers}")
        return {
            'method': self.method,
            'url': url,
            'params': self.get_params if self.method == 'GET' else None,
            'retry_params': self.retry_params,
            'data': self.get_params if self.method == 'POST' else None,
            'headers': self.headers,
        }
