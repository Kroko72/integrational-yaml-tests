import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ResponseChecker:
    """Проверяет ответ на соответствие ожидаемому результату."""

    def __init__(self, expected_result: Dict[str, Any]) -> None:
        self.expected_result = expected_result

    def check_result(self, response: requests.Response) -> None:
        logger.info('Checking response')
        try:
            actual_result = response.json() if 'application/json' in response.headers.get('Content-Type',
                                                                                          '') else response.text
            logger.debug(f"Actual response: {actual_result}")
            if actual_result == self.expected_result:
                logger.info("Test passed!")
            else:
                logger.error("Test failed!")
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            raise
