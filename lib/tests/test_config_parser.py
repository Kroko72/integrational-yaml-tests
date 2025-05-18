import unittest
import tempfile
from pathlib import Path
from lib.config_parser import ConfigParser


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.yaml_content = """
        config:
          scheme: https
          host: api.example.com
        """
        self.json_content = '{"config": {"scheme": "https", "host": "api.example.com"}}'

    def test_yaml_file_parsing(self):
        with tempfile.NamedTemporaryFile(suffix=".yaml") as f:
            f.write(self.yaml_content.encode())
            f.seek(0)
            parser = ConfigParser(file_path=f.name)
            self.assertEqual(parser.config["config"]["scheme"], "https")

    def test_json_file_parsing(self):
        with tempfile.NamedTemporaryFile(suffix=".json") as f:
            f.write(self.json_content.encode())
            f.seek(0)
            parser = ConfigParser(file_path=f.name)
            self.assertEqual(parser.config["config"]["host"], "api.example.com")

    def test_invalid_file_format(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as f:
            with self.assertRaises(ValueError):
                ConfigParser(file_path=f.name)


if __name__ == "__main__":
    unittest.main()
