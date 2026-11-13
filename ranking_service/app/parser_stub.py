"""Заглушка Parser service: имитирует данные из External Shops.

В реальной системе здесь работает отдельный воркер (Scrapy/httpx),
который по расписанию складывает предложения в БД.
"""
from decimal import Decimal

from .ranking import Offer

_OFFERS = [
    Offer("Джинсы slim fit", "ShopA", Decimal("49.90"), Decimal("4.99"), "EUR", "https://shop-a.example/jeans"),
    Offer("Джинсы slim fit", "ShopB", Decimal("52.00"), Decimal("0"), "USD", "https://shop-b.example/jeans"),
    Offer("Джинсы slim fit", "ShopC", Decimal("4200"), Decimal("350"), "RUB", "https://shop-c.example/jeans"),
    Offer("Джинсы slim fit", "ShopD", Decimal("39.00"), Decimal("9.00"), "GBP", "https://shop-d.example/jeans"),
    Offer("Худи оверсайз", "ShopA", Decimal("35.00"), Decimal("4.99"), "EUR", "https://shop-a.example/hoodie"),
    Offer("Худи оверсайз", "ShopB", Decimal("38.00"), Decimal("3.00"), "USD", "https://shop-b.example/hoodie"),
    Offer("Худи оверсайз", "ShopE", Decimal("30.00"), Decimal("5.00"), "XXX", "https://shop-e.example/hoodie"),
]


def search_offers(query: str):
    q = query.strip().lower()
    return [o for o in _OFFERS if q in o.title.lower()]
