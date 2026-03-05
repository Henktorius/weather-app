"""
api_client.py
-------------
Provides functions to fetch weather data from the Open-Meteo API.

Flow:
  1. Geocode a city name → (latitude, longitude)
  2. Fetch daily forecast for a specific date → max/min temp + weather condition
"""

import datetime
import requests

# ── Open-Meteo endpoints ──────────────────────────────────────────────────────
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# ── WMO Weather interpretation codes (WW) ─────────────────────────────────────
# Reference: https://open-meteo.com/en/docs  →  "WMO Weather interpretation codes"
WMO_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def interpret_weathercode(code: int) -> str:
    """Convert a WMO weather code to a human-readable string."""
    return WMO_CODES.get(code, "Unknown")


# ── Geocoding ─────────────────────────────────────────────────────────────────

def get_coordinates(city_name: str) -> tuple[float, float]:
    """
    Use the Open-Meteo Geocoding API to resolve *city_name* into
    geographic coordinates.

    Returns
    -------
    tuple[float, float]
        (latitude, longitude)

    Raises
    ------
    ValueError
        If the city cannot be found.
    ConnectionError / Exception
        If the HTTP request itself fails.
    """
    response = requests.get(
        GEOCODING_URL,
        params={"name": city_name, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])
    if not results:
        raise ValueError(f"City not found: {city_name}")

    first = results[0]
    return float(first["latitude"]), float(first["longitude"])


# ── Weather forecast ──────────────────────────────────────────────────────────

def get_weather(city_name: str, date: datetime.date) -> dict:
    """
    Fetch the daily weather forecast for *city_name* on *date*.

    Returns
    -------
    dict
        {
            "city":      str,
            "date":      str   (ISO format),
            "max_temp":  float,
            "min_temp":  float,
            "condition": str,
        }
        If the API has no data for the requested date the temperatures are
        set to ``None`` and ``condition`` is ``"Data Unavailable"`` (REQ-2.2).

    Raises
    ------
    ValueError
        If the city cannot be geocoded.
    """
    lat, lon = get_coordinates(city_name)

    date_str = date.isoformat()

    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": date_str,
            "end_date": date_str,
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    daily = data.get("daily", {})
    times = daily.get("time", [])

    if not times:
        return {
            "city": city_name,
            "date": date_str,
            "max_temp": None,
            "min_temp": None,
            "condition": "Data Unavailable",
        }

    max_temp = daily["temperature_2m_max"][0]
    min_temp = daily["temperature_2m_min"][0]
    weathercode = daily["weathercode"][0]

    return {
        "city": city_name,
        "date": date_str,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "condition": interpret_weathercode(weathercode),
    }
