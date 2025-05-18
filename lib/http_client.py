import logging
import requests
import time
from typing import Dict, Any


logger = logging.getLogger(__name__)


class HttpClient:
    """Отправляет HTTP-запросы с поддержкой повторных попыток."""

    def __init__(self, max_retries: int = 3, retry_delay: float = 1, backoff_factor: float = 2):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
        self.retry_status_codes = {500, 502, 503, 504}

    def send_request(self, request_data: Dict[str, Any]) -> requests.Response:
        method = request_data.pop('method')
        url = request_data.pop('url')

        for attempt in range(self.max_retries + 1):
            try:
                response = self._execute_request(method, url, request_data)
                if response.status_code < 500 or attempt == self.max_retries:
                    return response

                logger.warning(f"Retrying... Attempt {attempt + 1}/{self.max_retries}")
                self._wait_before_retry(attempt)

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt == self.max_retries:
                    raise
                self._wait_before_retry(attempt)

        return response  # type: ignore

    def _execute_request(self, method: str, url: str, params: Dict[str, Any]) -> requests.Response:
        if method == 'GET':
            return requests.get(url, **params)
        elif method == 'POST':
            return requests.post(url, **params)
        # Добавьте другие методы при необходимости
        raise ValueError(f"Unsupported method: {method}")

    def _wait_before_retry(self, attempt: int) -> None:
        delay = self.retry_delay * (self.backoff_factor ** attempt)
        logger.debug(f"Waiting {delay:.2f} seconds before next attempt")
        time.sleep(delay)
