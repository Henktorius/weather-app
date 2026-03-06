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


def test_city_entry_component(app):
    """Check if the city entry component is present."""
    app.root.update()
    city_label = app.root.nametowidget("cityinput_label")
    assert city_label.winfo_exists()
    city_textfield = app.root.nametowidget("city_entry")
    assert city_textfield.winfo_exists()


def test_startdate_label_component(app):
    """Check if the start date label component is present."""
    app.root.update()
    startdate_label = app.root.nametowidget("startdate_label")
    assert startdate_label.winfo_exists()


def test_submit_btn_component(app):
    """Check if the submit button component is present."""
    app.root.update()
    submit_btn = app.root.nametowidget("submit_btn")
    assert submit_btn.winfo_exists()


def test_duration_entry_component(app):
    """Check if the duration entry component is present."""
    app.root.update()
    duration_label = app.root.nametowidget("duration_label")
    assert duration_label.winfo_exists()
    duration_entry = app.root.nametowidget("duration_entry")
    assert duration_entry.winfo_exists()


def test_forecast_container_component(app):
    """Check if the forecast container component is present."""
    app.root.update()
    forecast_container = app.root.nametowidget("forecast_container")
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
