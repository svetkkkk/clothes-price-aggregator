from decimal import Decimal

import pytest

from app.currency import CurrencyConverter, UnknownCurrencyError
from app.ranking import Offer, rank_offers

conv = CurrencyConverter()


def offer(shop, price, delivery, cur="EUR", title="Футболка"):
    return Offer(title, shop, Decimal(price), Decimal(delivery), cur)


def test_convert_same_currency():
    assert conv.convert("10", "EUR", "EUR") == Decimal("10.00")


def test_convert_usd_to_eur():
    assert conv.convert("100", "USD", "EUR") == Decimal("92.00")


def test_convert_unknown_currency():
    with pytest.raises(UnknownCurrencyError):
        conv.convert("1", "XXX", "EUR")


def test_sorted_by_total_price_with_delivery():
    offers = [
        offer("A", "10", "5"),    # 15
        offer("B", "12", "0"),    # 12
        offer("C", "20", "1"),    # 21
    ]
    ranked, _ = rank_offers(offers, conv)
    assert [r.offer.shop for r in ranked] == ["B", "A", "C"]
    assert [r.position for r in ranked] == [1, 2, 3]


def test_delivery_can_change_order():
    # дешёвый товар с дорогой доставкой проигрывает
    offers = [offer("cheap_item", "10", "20"), offer("fair", "15", "2")]
    ranked, _ = rank_offers(offers, conv)
    assert ranked[0].offer.shop == "fair"


def test_mixed_currencies():
    offers = [
        offer("A", "50", "0", "EUR"),   # 50.00
        offer("B", "50", "0", "USD"),   # 46.00
        offer("C", "5000", "0", "RUB"), # 50.00
    ]
    ranked, _ = rank_offers(offers, conv)
    assert ranked[0].offer.shop == "B"
    assert ranked[0].total == Decimal("46.00")


def test_tie_broken_by_cheaper_delivery():
    offers = [offer("A", "8", "2"), offer("B", "9", "1")]  # оба 10
    ranked, _ = rank_offers(offers, conv)
    assert ranked[0].offer.shop == "B"


def test_invalid_offers_are_skipped_not_fatal():
    offers = [
        offer("ok", "10", "1"),
        offer("bad_cur", "10", "1", "XXX"),
        offer("negative", "-5", "1"),
    ]
    ranked, skipped = rank_offers(offers, conv)
    assert [r.offer.shop for r in ranked] == ["ok"]
    assert {o.shop for o, _ in skipped} == {"bad_cur", "negative"}


def test_empty_input():
    assert rank_offers([], conv) == ([], [])


def test_target_currency():
    ranked, _ = rank_offers([offer("A", "46", "0", "EUR")], conv, "USD")
    assert ranked[0].currency == "USD"
    assert ranked[0].total == Decimal("50.00")
