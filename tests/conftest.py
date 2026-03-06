import tkinter as tk
import pytest
from src.weather_app import WeatherApp


@pytest.fixture(scope="session")
def app():
    """Single shared Tk root for all GUI tests (avoids Tcl corruption)."""
    root = tk.Tk()
    application = WeatherApp(root)
    yield application
    root.destroy()
