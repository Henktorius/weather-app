import datetime
import tkinter as tk
from unittest.mock import patch
import pytest

class TestEmptyTrip:
    """Tests for the 'Empty Trip' functionality and button state."""

    def test_empty_button_initial_state(self, app):
        """The 'Empty Trip' button should be disabled by default."""
        empty_btn = app.root.nametowidget("delete_btn")
        assert str(empty_btn.cget("state")) == "disabled"

    @patch("src.weather_app.get_weather")
    def test_empty_button_enabled_after_adding_data(self, mock_get_weather, app):
        """The button should become enabled once weather data is successfully added."""
        mock_get_weather.return_value = [{"max_temp": 20.0}]
        
        # Add data to the app
        app.city_input.insert(0, "London")
        app.duration_input.delete(0, tk.END)
        app.duration_input.insert(0, "1")
        app.get_data()

        empty_btn = app.root.nametowidget("delete_btn")
        assert str(empty_btn.cget("state")) == "normal"

    @patch("src.weather_app.get_weather")
    def test_empty_trip_clears_forecast_rows(self, mock_get_weather, app):
        """Ensure only the header remains in the forecast container after clearing."""
        mock_get_weather.return_value = [{"max_temp": 20.0}, {"max_temp": 22.0}]
        
        # Populate with 2 days of data
        app.city_input.insert(0, "Paris")
        app.duration_input.delete(0, tk.END)
        app.duration_input.insert(0, "2")
        app.get_data()

        # Verify rows exist (1 header + 2 data rows)
        forecast_container = app.root.nametowidget("forecast_container")
        assert len(forecast_container.winfo_children()) == 2

        # Trigger the empty_trip function
        app.empty_trip()
        app.root.update()

        # Only the header should remain
        assert len(forecast_container.winfo_children()) == 1 #

    def test_empty_trip_resets_internal_state(self, app):
        """Check if internal counters and data lists are reset."""
        # Manually simulate some data
        app.trip.add_day(("Berlin", "25°C"))
        app.forecast_row_count = 1
        
        app.empty_trip()

        assert len(app.trip.days) == 0
        assert app.forecast_row_count == 0

    @patch("src.weather_app.get_weather")
    def test_empty_button_interaction(self, mock_get_weather, app):
        """Testing the actual button click (invoke) triggers the reset."""
        mock_get_weather.return_value = [{"max_temp": 15.0}]
        app.city_input.insert(0, "Oslo")
        app.get_data()
        
        empty_btn = app.root.nametowidget("delete_btn")
        
        # Simulate user clicking the button
        empty_btn.invoke()
        
        # Check if button is disabled again after click
        assert str(empty_btn.cget("state")) == "disabled"
        assert len(app.trip.days) == 0
