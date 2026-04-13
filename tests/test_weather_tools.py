# tests/test_weather_tools.py
from src.myagent.tools.weather import geocode_city, get_weather


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_geocode_city(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert "geocoding-api.open-meteo.com" in url
        assert params["name"] == "Berlin"
        return DummyResponse({
            "results": [
                {
                    "name": "Berlin",
                    "country": "Germany",
                    "latitude": 52.52437,
                    "longitude": 13.41053,
                }
            ]
        })

    monkeypatch.setattr("src.myagent.tools.weather.requests.get", fake_get)

    result = geocode_city("Berlin")
    assert result["name"] == "Berlin"
    assert result["country"] == "Germany"
    assert result["latitude"] == 52.52437
    assert result["longitude"] == 13.41053


def test_geocode_city_raises_on_no_results(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        return DummyResponse({"results": []})

    monkeypatch.setattr("src.myagent.tools.weather.requests.get", fake_get)

    try:
        geocode_city("NoSuchCity")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "No location found" in str(exc)


def test_get_weather(monkeypatch):
    def fake_get(url, params=None, timeout=10):
        assert "api.open-meteo.com" in url
        assert params["latitude"] == 52.52
        assert params["longitude"] == 13.41
        return DummyResponse({
            "current": {
                "temperature_2m": 12.3,
                "apparent_temperature": 10.8,
                "precipitation": 0.2,
                "rain": 0.2,
                "showers": 0.0,
                "snowfall": 0.0,
                "weather_code": 61,
                "wind_speed_10m": 14.1,
            }
        })

    monkeypatch.setattr("src.myagent.tools.weather.requests.get", fake_get)

    result = get_weather(52.52, 13.41)
    assert result["temperature_2m"] == 12.3
    assert result["weather_code"] == 61
    assert result["wind_speed_10m"] == 14.1