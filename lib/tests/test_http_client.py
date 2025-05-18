import unittest
from unittest.mock import patch, Mock
from lib.http_client import HttpClient


class TestHttpClient(unittest.TestCase):
    @patch('modules.http_client.requests')
    def test_send_get_request(self, mock_requests):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response

        client = HttpClient()
        request_data = {
            "method": "GET",
            "url": "https://api.example.com/users",
            "headers": {}
        }

        response = client.send_request(request_data)
        self.assertEqual(response.status_code, 200)

    def test_retry_mechanism(self):
        with patch('modules.http_client.requests.get') as mock_get:
            mock_get.side_effect = [
                Mock(status_code=500),
                Mock(status_code=200)
            ]

            client = HttpClient(max_retries=2)
            response = client.send_request({
                "method": "GET",
                "url": "https://api.example.com"
            })

            assert mock_get.call_count == 2
            assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
