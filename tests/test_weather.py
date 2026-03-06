import tkinter as tk
import pytest
from src.weather_app import WeatherApp


@pytest.fixture
def app():
    """Fixture to initialize the tk root and the app."""
    root = tk.Tk()
    app = WeatherApp(root)
    yield app
    # Clean up after the test is done
    root.destroy()


# TODO: Add integration test later
