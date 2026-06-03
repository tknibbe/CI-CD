# tests/test_app.py
import pytest
from App.App import App, db


@pytest.fixture
def client():
    db.clear()
    App.config["TESTING"] = True
    with App.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_shorten_happy(client):
    res = client.post("/shorten",  json={"url": "https://google.com"})
    assert res.status_code == 201
    assert "code" in res.get_json()
    assert "short_url" in res.get_json()


def test_shorten_double(client):
    res = client.post("/shorten",  json={"url": "https://google.com"})
    res = client.post("/shorten",  json={"url": "https://google.com"})
    assert res.status_code == 200
    assert "code" in res.get_json()
    assert "short_url" in res.get_json()


def test_shorten_no_URL(client):
    res = client.post("/shorten")
    assert res.status_code == 400


def test_shorten_nvalid_URL(client):
    res = client.post("/shorten", json={"url": "google.com"})
    assert res.status_code == 400


def test_redirect_happy(client):
    res = client.post("/shorten",  json={"url": "https://google.com"})
    data = res.get_json()
    code = data.get("short_url")
    res = client.get(code)
    assert res.status_code == 302


def test_redirect_unknown_code(client):
    code = "unknown_code"
    res = client.get(code)
    assert res.status_code == 404
