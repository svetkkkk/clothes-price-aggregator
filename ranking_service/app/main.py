"""Backend/API: GET /api/ranking?query=...&currency=EUR"""
from fastapi import FastAPI, HTTPException, Query

from .cache import build_cache
from .currency import CurrencyConverter
from .parser_stub import search_offers
from .ranking import rank_offers

app = FastAPI(title="Рейтинг предложений по цене с доставкой")
converter = CurrencyConverter()
cache = build_cache()


@app.get("/api/ranking")
def ranking(query: str = Query(..., min_length=2), currency: str = "EUR"):
    currency = currency.upper()
    if currency not in converter.supported:
        raise HTTPException(400, f"Валюта не поддерживается. Доступны: {converter.supported}")

    key = f"ranking:{query.strip().lower()}:{currency}"
    cached = cache.get(key)
    if cached is not None:
        return {**cached, "cached": True}

    ranked, skipped = rank_offers(search_offers(query), converter, currency)
    payload = {
        "query": query,
        "currency": currency,
        "items": [
            {
                "position": r.position,
                "title": r.offer.title,
                "shop": r.offer.shop,
                "price": str(r.price),
                "delivery": str(r.delivery),
                "total": str(r.total),
                "url": r.offer.url,
            }
            for r in ranked
        ],
        "skipped": [{"shop": o.shop, "reason": why} for o, why in skipped],
    }
    cache.set(key, payload)
    return {**payload, "cached": False}
