import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_ranking_endpoint_sorted_and_cached():
    r1 = client.get("/api/ranking", params={"query": "джинсы"})
    assert r1.status_code == 200
    totals = [float(i["total"]) for i in r1.json()["items"]]
    assert totals == sorted(totals) and len(totals) == 4
    assert r1.json()["cached"] is False

    r2 = client.get("/api/ranking", params={"query": "джинсы"})
    assert r2.json()["cached"] is True


def test_skipped_shop_reported():
    r = client.get("/api/ranking", params={"query": "худи"})
    assert [s["shop"] for s in r.json()["skipped"]] == ["ShopE"]


def test_unsupported_currency():
    r = client.get("/api/ranking", params={"query": "джинсы", "currency": "JPY"})
    assert r.status_code == 400


def test_short_query_rejected():
    assert client.get("/api/ranking", params={"query": "а"}).status_code == 422
