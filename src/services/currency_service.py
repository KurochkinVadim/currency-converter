import requests
import os
from typing import Optional

class CurrencyService:
    def __init__(self):
        self.base_url = "https://api.frankfurter.app/latest"
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float | None:
        """
        Получает курс обмена через Frankfurter API (бесплатный)
        """
        try:
            # Для тестирования, если API недоступно
            if from_currency == to_currency:
                return 1.0
            if from_currency == "RUB" or to_currency == "RUB":
                return self._get_fallback_rate(from_currency, to_currency)
                
            response = requests.get(f"{self.base_url}?from={from_currency}&to={to_currency}")
            
            if response.status_code == 200:
                data = response.json()
                return data['rates'].get(to_currency)
            else:
                # Fallback: фиктивные курсы для демонстрации
                return self._get_fallback_rate(from_currency, to_currency)
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            return self._get_fallback_rate(from_currency, to_currency)
    
    def _get_fallback_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Фиктивные курсы для демонстрации, если API недоступно
        """
        rates = {
            "USD": {"EUR": 0.85, "GBP": 0.75, "JPY": 110.0, "RUB": 90.0},
            "EUR": {"USD": 1.18, "GBP": 0.88, "JPY": 130.0, "RUB": 105.0},
            "GBP": {"USD": 1.33, "EUR": 1.14, "JPY": 150.0, "RUB": 120.0},
            "JPY": {"USD": 0.0091, "EUR": 0.0077, "GBP": 0.0067, "RUB": 0.82},
            "RUB": {"USD": 0.011, "EUR": 0.0095, "GBP": 0.0083, "JPY": 1.22}
        }

        if from_currency in rates and to_currency in rates[from_currency]:
            return rates[from_currency][to_currency]
        else:
            return 1.0  # По умолчанию

currency_service = CurrencyService()