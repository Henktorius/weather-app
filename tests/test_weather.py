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


def test_initial_label(app):
    """Check if the starting text is correct."""
    assert app.label.cget("text") == "Enter City:"


def test_button_click_updates_label(app):
    """Simulate user input and a button click."""
    # 1. Simulate typing into the Entry widget
    app.city_input.insert(0, "London")

    # 2. Manually trigger the button command
    app.submit_btn.invoke()

    # 3. Force Tkinter to process the change
    app.root.update()

    # 4. Assert the result
    assert app.label.cget("text") == "Weather for London"


