import datetime
import tkinter as tk
from unittest.mock import patch

@patch('src.weather_app.get_weather')
def test_weather_data(mock_get_weather, app):
    app.root.update()

    # Mock the weather data
    mock_get_weather.return_value = [
        {"date": "2026-03-10", "max_temp": 15.0, "min_temp": 5.0, "condition": "Clear sky"},
        {"date": "2026-03-11", "max_temp": 16.0, "min_temp": 6.0, "condition": "Partly cloudy"}
    ]

    city = app.root.nametowidget("city_entry")
    city.delete(0, tk.END)
    city.insert(0, "Karlskrona")

    duration = app.root.nametowidget("duration_entry")
    duration.delete(0, tk.END)
    duration.insert(0, "2")

    date = app.startdatepicker
    date.set_date(datetime.date(2026, 3, 10))

    # Before submit, trip should be empty
    assert len(app.trip) == 0 

    app.submit_btn.invoke()

    # After submit, check that data was added to the data structure
    assert len(app.trip) == 2
    days = app.trip.get_days()
    assert days[0][0] == "Karlskrona (2026-03-10)"
    assert days[0][1] == "15.0°C"
    assert days[1][0] == "Karlskrona (2026-03-11)"
    assert days[1][1] == "16.0°C"