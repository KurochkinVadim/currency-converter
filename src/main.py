from fastapi import FastAPI, Response
from prometheus_client import generate_latest, Counter, Histogram
import time

from .routers import converter
from .database import engine, Base

# Создаём метрики для мониторинга
REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

app = FastAPI(
    title="Currency Converter API", 
    description="Simple currency conversion service with history and monitoring",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(converter.router)

# Ручной эндпоинт для метрик без редиректа
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/")
async def root():
    with REQUEST_LATENCY.time():
        REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
        return {
            "message": "Currency Converter API is running!",
            "endpoints": {
                "docs": "/docs",
                "health": "/health", 
                "convert": "/api/v1/convert",
                "history": "/api/v1/history",
                "currencies": "/api/v1/currencies"
            }
        }

@app.get("/health")
async def health_check():
    with REQUEST_LATENCY.time():
        REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
        return {"status": "healthy", "database": "connected"}