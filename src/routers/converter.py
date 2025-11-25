from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from prometheus_client import Counter, Histogram

from ..models.currency_models import ConversionRequest, ConversionResponse, ConversionHistory
from ..services.currency_service import currency_service
from ..database import get_db, ConversionRecord

router = APIRouter(prefix="/api/v1", tags=["currency"])

CONVERSION_COUNT = Counter('conversion_count', 'Currency Conversion Count', ['from_currency', 'to_currency'])
CONVERSION_LATENCY = Histogram('conversion_latency_seconds', 'Conversion latency')

@router.post("/convert", response_model=ConversionResponse)
async def convert_currency(
    request: ConversionRequest,
    db: Session = Depends(get_db)
):
    with CONVERSION_LATENCY.time():
        # Получаем курс обмена
        rate = currency_service.get_exchange_rate(request.from_currency.upper(), request.to_currency.upper())

        if rate is None:
            raise HTTPException(status_code=400, detail="Unable to get exchange rate")
        
        # Вычисляем конвертированную сумму
        converted_amount = request.amount * rate
        
        # Сохраняем в базу данных
        db_record = ConversionRecord(
            amount=request.amount,
            from_currency=request.from_currency.upper(),
            to_currency=request.to_currency.upper(),
            converted_amount=converted_amount,
            rate=rate
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        CONVERSION_COUNT.labels(
            from_currency=request.from_currency.upper(),
            to_currency=request.to_currency.upper()
        ).inc()
        
        return ConversionResponse(
            amount=request.amount,
            from_currency=request.from_currency.upper(),
            to_currency=request.to_currency.upper(),
            converted_amount=converted_amount,
            rate=rate,
            timestamp=db_record.timestamp
        )

@router.get("/history", response_model=list[ConversionHistory])
async def get_conversion_history(db: Session = Depends(get_db)):
    records = db.query(ConversionRecord).order_by(ConversionRecord.timestamp.desc()).limit(10).all()
    
    return [
        ConversionHistory(
            id=record.id,
            amount=record.amount,
            from_currency=record.from_currency,
            to_currency=record.to_currency,
            converted_amount=record.converted_amount,
            rate=record.rate,
            timestamp=record.timestamp
        )
        for record in records
    ]

@router.get("/currencies")
async def get_available_currencies():
    """
    Возвращает список доступных валют
    """
    return {
        "available_currencies": ["USD", "EUR", "GBP", "JPY", "RUB"],
        "source": "Frankfurter API + Fallback",
        "supported_pairs": [
            "USD-RUB", "EUR-RUB", "GBP-RUB", "JPY-RUB",
            "RUB-USD", "RUB-EUR", "RUB-GBP", "RUB-JPY"
        ]
    }