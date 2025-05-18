import unittest
from unittest.mock import Mock
from lib.response_checker import ResponseChecker


class TestResponseChecker(unittest.TestCase):
    def setUp(self):
        self.response = Mock()
        self.response.headers = {"Content-Type": "application/json"}

    def test_successful_json_check(self):
        self.response.json.return_value = {"id": 1}
        checker = ResponseChecker({"id": 1})
        checker.check_result(self.response)
        # Проверяем через логи или добавляем ассерты

    def test_failed_check(self):
        self.response.json.return_value = {"id": 2}
        checker = ResponseChecker({"id": 1})
        with self.assertLogs(level='ERROR') as log:
            checker.check_result(self.response)
            self.assertIn("Test failed!", log.output[0])


if __name__ == "__main__":
    unittest.main()
