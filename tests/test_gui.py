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


def test_components(app):
    """Check if the required components are present."""
    app.root.update()  # Ensure all components are rendered

    city_textfield = app.root.nametowidget("city_entry")
    startdate_label = app.root.nametowidget("startdate_label")
    submit_btn = app.root.nametowidget("submit_btn")
    duration_label = app.root.nametowidget("duration_label")
    duration_entry = app.root.nametowidget("duration_entry")
    forecast_container = app.root.nametowidget("forecast_container")

    assert city_textfield.winfo_exists()
    assert startdate_label.winfo_exists()
    assert submit_btn.winfo_exists()
    assert duration_label.winfo_exists()
    assert duration_entry.winfo_exists()
    assert forecast_container.winfo_exists()


def test_data_display(app):
    """Check if the label updates correctly when a city is entered and the button is clicked."""
    app.root.update()
    app.forecast_container.update()
    app.update_label()  # Simulate button click to update the label with the city data
    rows = app.forecast_container.winfo_children()
    assert len(rows) == 0

    # fill datastructure
    app.trip.add_day(("Karlskrona", 15.0))

    # check if city is added to the forecast container
    app.forecast_container.update()
    app.update_label()
    rows = app.forecast_container.winfo_children()
    assert len(rows) == 1
    assert rows[0].winfo_children()[0].cget("text") == "Karlskrona"
    assert rows[0].winfo_children()[1].cget("text") == 15.0

    # add another city and check if it is added to the forecast container
    app.trip.add_day(("Stockholm", 20.0))
    app.forecast_container.update()
    app.update_label()
    rows = app.forecast_container.winfo_children()
    assert len(rows) == 2
    assert rows[0].winfo_children()[0].cget("text") == "Karlskrona"
    assert rows[0].winfo_children()[1].cget("text") == 15.0
    assert rows[1].winfo_children()[0].cget("text") == "Stockholm"
    assert rows[1].winfo_children()[1].cget("text") == 20.0
