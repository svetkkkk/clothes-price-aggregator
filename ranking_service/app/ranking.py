"""Ядро функции: рейтинг товаров по итоговой цене (цена + доставка)."""
from dataclasses import dataclass
from decimal import Decimal

from .currency import CurrencyConverter, UnknownCurrencyError


@dataclass(frozen=True)
class Offer:
    title: str
    shop: str
    price: Decimal
    delivery: Decimal
    currency: str
    url: str = ""


@dataclass(frozen=True)
class RankedOffer:
    position: int
    offer: Offer
    price: Decimal      # в целевой валюте
    delivery: Decimal   # в целевой валюте
    total: Decimal      # цена + доставка
    currency: str


def rank_offers(offers, converter: CurrencyConverter, target_currency="EUR"):
    """Возвращает (рейтинг, пропущенные).

    Рейтинг отсортирован от самого дешёвого к самому дорогому по цене с
    доставкой. При равенстве выигрывает более дешёвая доставка, затем
    порядок по названию (чтобы результат был детерминированным).
    Некорректные предложения (отрицательные суммы, неизвестная валюта)
    пропускаются и возвращаются отдельно, а не ломают весь рейтинг.
    """
    target = target_currency.upper()
    converted, skipped = [], []

    for offer in offers:
        if offer.price < 0 or offer.delivery < 0:
            skipped.append((offer, "отрицательная цена или доставка"))
            continue
        try:
            price = converter.convert(offer.price, offer.currency, target)
            delivery = converter.convert(offer.delivery, offer.currency, target)
        except UnknownCurrencyError as exc:
            skipped.append((offer, str(exc)))
            continue
        converted.append((offer, price, delivery, price + delivery))

    converted.sort(key=lambda x: (x[3], x[2], x[0].title))

    ranked = [
        RankedOffer(i, o, p, d, t, target)
        for i, (o, p, d, t) in enumerate(converted, start=1)
    ]
    return ranked, skipped
