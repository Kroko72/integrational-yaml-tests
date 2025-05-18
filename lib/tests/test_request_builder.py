import unittest
from lib.request_builder import RequestBuilder


class TestRequestBuilder(unittest.TestCase):
    def test_build_get_request(self):
        config = {
            "config": {
                "scheme": "https",
                "host": "api.example.com",
                "path": "/users",
                "method": "GET",
                "port": 8080
            },
            "headers": {"Authorization": "Bearer token"}
        }

        builder = RequestBuilder(config)
        request = builder.build_request()

        self.assertEqual(request["url"], "https://api.example.com:8080/users")
        self.assertEqual(request["method"], "GET")
        self.assertEqual(request["headers"]["Authorization"], "Bearer token")


if __name__ == "__main__":
    unittest.main()
