# Currency Converter API

Простой микросервис для конвертации валют с мониторингом и историей операций.

## Функциональность

- Конвертация валют (USD, EUR, GBP, JPY, RUB)
- История конвертаций
- Мониторинг через Prometheus + Grafana
- Автоматическая документация Swagger

## Запуск

```bash
docker-compose up --build

API Endpoints
GET / - информация о сервисе

GET /health - health check

POST /api/v1/convert - конвертация валют

GET /api/v1/history - история операций

GET /api/v1/currencies - список валют

GET /metrics - метрики Prometheus
```

## CI/CD Pipeline

Проект использует GitLab CI/CD с симуляцией двух машин:

- **Сборка**: Локальный GitLab Runner
- **Деплой**: "Продакшен" окружение на портах 8001, 9091, 3001

### Запуск CI/CD локально:

```bash
# Запуск GitLab Runner
docker run -d --name gitlab-runner --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/.gitlab-runner-config.toml:/etc/gitlab-runner/config.toml \
  gitlab/gitlab-runner:latest

# Проверка статуса
docker logs gitlab-runner