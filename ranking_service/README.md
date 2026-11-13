# Рейтинг предложений по цене с доставкой

Функция из практики 1: сайт собирает предложения магазинов и выстраивает их
от самого дешёвого (цена + доставка) к самому дорогому.

## Запуск
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    # http://127.0.0.1:8000/api/ranking?query=джинсы&currency=EUR
    # документация: http://127.0.0.1:8000/docs

Redis подключается через переменную `REDIS_URL` (например `redis://localhost:6379/0`).
Без неё работает кэш в памяти.

## Тесты
    pytest -v

## Структура
- `app/currency.py`    Currency Converter
- `app/ranking.py`     ядро: сортировка по итоговой цене
- `app/parser_stub.py` заглушка Parser service / External Shops
- `app/cache.py`       Redis-кэш (с запасным вариантом в памяти)
- `app/main.py`        Backend/API (FastAPI)
