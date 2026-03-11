import tkinter as tk
import pytest
import src.api_client
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

    # Clear the UI elements created during previous tests
    for widget in _app_session.forecast_container.winfo_children():
        widget.destroy()

    yield _app_session
