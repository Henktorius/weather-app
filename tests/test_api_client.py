import pytest
import datetime
from unittest.mock import patch, MagicMock
from src.api_client import get_coordinates, get_weather, interpret_weathercode


# ---------------------------------------------------------------------------
# WMO Weather Code Interpretation
# ---------------------------------------------------------------------------

class TestInterpretWeathercode:
    """Test the mapping from WMO weather codes to human-readable strings."""

    def test_clear_sky(self):
        assert interpret_weathercode(0) == "Clear sky"

    def test_rain_code(self):
        assert interpret_weathercode(61) == "Slight rain"

    def test_snow_code(self):
        assert interpret_weathercode(71) == "Slight snow fall"

    def test_unknown_code_returns_string(self):
        """An unrecognised code should still return a non-empty string."""
        result = interpret_weathercode(9999)
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# get_coordinates
# ---------------------------------------------------------------------------

class TestGetCoordinates:
    """Tests for geocoding a city name into (lat, lon)."""

    @patch("src.api_client.requests.get")
    def test_valid_city_returns_tuple(self, mock_get):
        """A known city should return a (latitude, longitude) tuple of floats."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": 2643743,
                    "name": "Karlskrona",
                    "latitude": 51.50853,
                    "longitude": -0.12574,
                    "country": "United Kingdom",
                }
            ]
        }
        mock_get.return_value = mock_response

        lat, lon = get_coordinates("Karlskrona")

        assert isinstance(lat, float)
        assert isinstance(lon, float)
        assert lat == pytest.approx(51.50853, abs=0.01)
        assert lon == pytest.approx(-0.12574, abs=0.01)

    @patch("src.api_client.requests.get")
    def test_invalid_city_raises_value_error(self, mock_get):
        """A city that does not exist should raise a ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # no "results" key
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="City not found"):
            get_coordinates("XYZNONEXISTENT")

    @patch("src.api_client.requests.get")
    def test_empty_results_raises_value_error(self, mock_get):
        """An empty results list should raise a ValueError."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="City not found"):
            get_coordinates("XYZNONEXISTENT")

    @patch("src.api_client.requests.get")
    def test_api_http_error_raises(self, mock_get):
        """A non-200 status code should raise a ConnectionError."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Server Error")
        mock_get.return_value = mock_response

        with pytest.raises(Exception):
            get_coordinates("Karlskrona")


# ---------------------------------------------------------------------------
# get_weather
# ---------------------------------------------------------------------------

class TestGetWeather:
    """Tests for fetching weather data for a city and date."""

    @patch("src.api_client.requests.get")
    def test_successful_response_structure(self, mock_get):
        """A successful call returns a dict with the expected keys and types."""
        # We need TWO HTTP calls: geocoding + forecast
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            "results": [
                {"name": "Karlskrona", "latitude": 51.5, "longitude": -0.1}
            ]
        }

        forecast_response = MagicMock()
        forecast_response.status_code = 200
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2026-03-10"],
                "temperature_2m_max": [15.2],
                "temperature_2m_min": [7.8],
                "weathercode": [3],
            }
        }

        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weather("Karlskrona", datetime.date(2026, 3, 10), datetime.date(2026, 3, 10))

        # Structure checks
        assert isinstance(result, list)
        assert len(result) == 1
        day = result[0]
        assert isinstance(day, dict)
        assert "city" in day
        assert "date" in day
        assert "max_temp" in day
        assert "min_temp" in day
        assert "condition" in day

    @patch("src.api_client.requests.get")
    def test_temperatures_are_numeric(self, mock_get):
        """max_temp and min_temp must be numbers (int or float)."""
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            "results": [
                {"name": "Berlin", "latitude": 52.52, "longitude": 13.41}
            ]
        }

        forecast_response = MagicMock()
        forecast_response.status_code = 200
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2026-03-10"],
                "temperature_2m_max": [18.5],
                "temperature_2m_min": [9.1],
                "weathercode": [0],
            }
        }
        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weather("Berlin", datetime.date(2026, 3, 10), datetime.date(2026, 3, 10))

        assert isinstance(result[0]["max_temp"], (int, float))
        assert isinstance(result[0]["min_temp"], (int, float))

    @patch("src.api_client.requests.get")
    def test_max_temp_greater_or_equal_min_temp(self, mock_get):
        """max_temp should be >= min_temp."""
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            "results": [
                {"name": "Madrid", "latitude": 40.42, "longitude": -3.70}
            ]
        }

        forecast_response = MagicMock()
        forecast_response.status_code = 200
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2026-03-10"],
                "temperature_2m_max": [22.0],
                "temperature_2m_min": [11.0],
                "weathercode": [1],
            }
        }
        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weather("Madrid", datetime.date(2026, 3, 10), datetime.date(2026, 3, 10))

        assert result[0]["max_temp"] >= result[0]["min_temp"]

    @patch("src.api_client.requests.get")
    def test_city_name_in_response(self, mock_get):
        """The returned dict should contain the requested city name."""
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            "results": [
                {"name": "Stockholm", "latitude": 59.33, "longitude": 18.07}
            ]
        }

        forecast_response = MagicMock()
        forecast_response.status_code = 200
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2026-03-10"],
                "temperature_2m_max": [5.0],
                "temperature_2m_min": [-1.0],
                "weathercode": [71],
            }
        }
        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weather("Stockholm", datetime.date(2026, 3, 10), datetime.date(2026, 3, 10))

        assert result[0]["city"] == "Stockholm"

    @patch("src.api_client.requests.get")
    def test_condition_is_string(self, mock_get):
        """The weather condition should be a human-readable string."""
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            "results": [
                {"name": "Oslo", "latitude": 59.91, "longitude": 10.75}
            ]
        }

        forecast_response = MagicMock()
        forecast_response.status_code = 200
        forecast_response.json.return_value = {
            "daily": {
                "time": ["2026-03-10"],
                "temperature_2m_max": [3.0],
                "temperature_2m_min": [-2.0],
                "weathercode": [61],
            }
        }
        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weather("Oslo", datetime.date(2026, 3, 10), datetime.date(2026, 3, 10))

        assert isinstance(result[0]["condition"], str)
        assert len(result[0]["condition"]) > 0

    @patch("src.api_client.requests.get")
    def test_missing_data_returns_unavailable(self, mock_get):
        """If the API returns no daily data, result should flag Data Unavailable (REQ-2.2)."""
        geo_response = MagicMock()
        geo_response.status_code = 200
        geo_response.json.return_value = {
            "results": [
                {"name": "Karlskrona", "latitude": 51.5, "longitude": -0.1}
            ]
        }

        forecast_response = MagicMock()
        forecast_response.status_code = 200
        forecast_response.json.return_value = {
            "daily": {
                "time": [],
                "temperature_2m_max": [],
                "temperature_2m_min": [],
                "weathercode": [],
            }
        }
        mock_get.side_effect = [geo_response, forecast_response]

        result = get_weather("Karlskrona", datetime.date(2030, 1, 1), datetime.date(2030, 1, 1))

        assert result[0]["condition"] == "Data Unavailable"

    @patch("src.api_client.requests.get")
    def test_invalid_city_raises(self, mock_get):
        """get_weather should propagate ValueError for an invalid city."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="City not found"):
            get_weather("XYZNONEXISTENT", datetime.date(2026, 3, 10), datetime.date(2026, 3, 10))
