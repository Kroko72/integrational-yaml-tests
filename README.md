# Мини библиотека для написания интеграционных тестов в формате yaml/json

считывает yaml/json файлы вида 

```yaml
config:
    version: 1
    host: 'localhost'
    port: 8080
    scheme: 'http'
    method: 'GET'
    path: '/test'
    retry:
        max_retries: 3    # Макс. попыток (по умолчанию: 3)
        retry_delay: 1    # Базовая задержка в секундах (по умолчанию: 1)
        backoff_factor: 2 # Множитель для экспоненциальной задержки (по умолчанию: 2)
get_params:
    a: 1
    b: 2
    c: 3
headers: 
    User-Agent: 'yaml-test-client'
result:
    test: 1
```

Делает запрос по пути, указанному в конфиге с нужными гет параметрами и проверять результат.

Польза - удобный способ писать интеграционные тесты.
