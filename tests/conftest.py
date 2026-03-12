import tkinter as tk

import pytest

from src.weather_app import WeatherApp


@pytest.fixture(scope="session")
def _app_session():
    """Single shared Tk root for all GUI tests."""
    root = tk.Tk()
    application = WeatherApp(root)
    yield application
    root.destroy()


@pytest.fixture(scope="function")
def app(_app_session):
    """Yields the session app but resets its data structures and UI before each test."""
    # Reset the trip data structure
    _app_session.trip.days.clear()
    _app_session.forecast_row_count = 0

    # Re-enable the start date picker
    _app_session.startdatepicker.configure(state="normal")

    # Re-enable inputs that may have been disabled at 14-day limit
    _app_session.submit_btn.configure(state="normal")
    _app_session.city_input.configure(state="normal")
    _app_session.duration_input.configure(state="normal", to=14)

    # Clear the UI elements created during previous tests
    for widget in _app_session.forecast_container.winfo_children():
        widget.destroy()

    yield _app_session
