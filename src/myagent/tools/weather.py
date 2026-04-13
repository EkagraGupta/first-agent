import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_city(city: str) -> dict:
    resp = requests.get(
        url=GEOCODE_URL,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

    results = data.get("results") or []
    if not results:
        raise ValueError(f"No location found in city={city}")
    
    hit = results[0]
    return {
        "name": hit["name"],
        "country": hit.get("country"),
        "latitude": hit["latitude"],
        "longitude": hit["longitude"],
    }


def get_weather(latitude: float, longitude: float) -> dict:
    resp = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,apparent_temperature,precipitation,"
                       "rain,showers,snowfall,weather_code,wind_speed_10m",
            "timezone": "auto",
        },
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

    current = data.get("current")
    if not current:
        raise ValueError("Weather response missing 'current'")

    return {
        "temperature_2m": current.get("temperature_2m"),
        "apparent_temperature": current.get("apparent_temperature"),
        "precipitation": current.get("precipitation"),
        "rain": current.get("rain"),
        "showers": current.get("showers"),
        "snowfall": current.get("snowfall"),
        "weather_code": current.get("weather_code"),
        "wind_speed_10m": current.get("wind_speed_10m"),
    }



if __name__=="__main__":
    # Test the functions
    city = "Dresden"
    location = geocode_city(city)
    print(f"Location for {city}: {location}")

    weather = get_weather(location["latitude"], location["longitude"])
    print(f"Current weather in {city}: {weather}")