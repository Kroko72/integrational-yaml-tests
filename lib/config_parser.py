import json
import logging
from typing import Optional, Dict, Any
import yaml


logger = logging.getLogger(__name__)


class ConfigParser:
    """Парсер для чтения конфигурации из YAML/JSON-файла или строки."""

    def __init__(self, file_path: Optional[str] = None, yaml_string: Optional[str] = None,
                 json_string: Optional[str] = None) -> None:
        if file_path:
            logger.info(f"Reading config from file: {file_path}")
            if file_path.endswith(('.yaml', '.yml')):
                self.config = self._parse_yaml_file(file_path)
            elif file_path.endswith('.json'):
                self.config = self._parse_json_file(file_path)
            else:
                logger.error("Unsupported file format")
                raise ValueError('Use .yaml, .yml, or .json.')
        elif yaml_string:
            logger.debug("Parsing YAML string")
            self.config = self._parse_yaml_string(yaml_string)
        elif json_string:
            logger.debug("Parsing JSON string")
            self.config = self._parse_json_string(json_string)
        else:
            logger.error("No input provided")
            raise ValueError('Provide file_path, yaml_string, or json_string.')

    # YAML-методы
    def _parse_yaml_file(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def _parse_yaml_string(self, yaml_string: str) -> Dict[str, Any]:
        return yaml.safe_load(yaml_string)

    # JSON-методы
    def _parse_json_file(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _parse_json_string(self, json_string: str) -> Dict[str, Any]:
        return json.loads(json_string)