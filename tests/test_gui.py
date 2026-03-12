import datetime
import tkinter as tk
from unittest.mock import patch

import pytest


class TestGUIComponents:
    """Check if all necessary components are present."""

    def test_city_entry_component(self, app):
        city_label = app.root.nametowidget("cityinput_label")
        assert city_label.winfo_exists()
        city_textfield = app.root.nametowidget("city_entry")
        assert city_textfield.winfo_exists()

    def test_startdate_label_component(self, app):
        startdate_label = app.root.nametowidget("startdate_label")
        assert startdate_label.winfo_exists()

    def test_submit_btn_component(self, app):
        submit_btn = app.root.nametowidget("submit_btn")
        assert submit_btn.winfo_exists()

    def test_duration_entry_component(self, app):
        duration_label = app.root.nametowidget("duration_label")
        assert duration_label.winfo_exists()
        duration_entry = app.root.nametowidget("duration_entry")
        assert duration_entry.winfo_exists()

    def test_forecast_container_component(self, app):
        forecast_container = app.root.nametowidget("forecast_container")
        assert forecast_container.winfo_exists()

    def test_bg_color(self, app):
        # Check that the background color of the root window is not the default gray
        assert app.root.cget("bg") != "SystemButtonFace"


class TestForecastDisplay:
    def test_initial_state(self, app):
        """Check that the forecast container is empty when the app starts."""
        app.root.update()
        forecast_container = app.root.nametowidget("forecast_container")
        assert len(forecast_container.winfo_children()) == 0

    def test_header_display(self, app):
        """Check that the forecast container displays the correct header."""
        app._create_forecast_container()
        app.forecast_container.update()
        rows = app.forecast_container.winfo_children()
        assert len(rows) == 1
        header_data = rows[0].winfo_children()
        assert header_data[0].cget("text") == "Day"
        assert header_data[1].cget("text") == ""
        assert header_data[2].cget("text") == "Date"
        assert header_data[3].cget("text") == "City"
        assert header_data[4].cget("text") == "Temperature"

    def test_column_content(self, app):
        """Check if the forecast container displays the correct column content."""

        app._add_forecast_row("Karlskrona", "5.0°C")
        app.forecast_container.update()
        rows = app.forecast_container.winfo_children()
        assert len(rows) == 1
        row_data = rows[0].winfo_children()
        assert row_data[0].cget("text") == "#1"
        assert row_data[1].cget("text") == datetime.date.today().strftime("%A")
        assert row_data[2].cget("text") == datetime.date.today().strftime("%d.%m.%Y")
        assert row_data[3].cget("text") == "Karlskrona"
        assert row_data[4].cget("text") == "5.0°C"

    def test_multiple_rows(self, app):
        """Check that multiple rows are added correctly to the forecast container."""
        app._add_forecast_row("Karlskrona", "5.0°C")
        app._add_forecast_row("Stockholm", "10.0°C")
        app.forecast_container.update()
        rows = app.forecast_container.winfo_children()
        assert len(rows) == 2
        row1_data = rows[0].winfo_children()
        row2_data = rows[1].winfo_children()
        assert row1_data[0].cget("text") == "#1"
        assert row1_data[1].cget("text") == datetime.date.today().strftime("%A")
        assert row1_data[2].cget("text") == datetime.date.today().strftime("%d.%m.%Y")
        assert row2_data[0].cget("text") == "#2"
        assert row2_data[1].cget("text") == (
            datetime.date.today() + datetime.timedelta(days=1)
        ).strftime("%A")
        assert row2_data[2].cget("text") == (
            datetime.date.today() + datetime.timedelta(days=1)
        ).strftime("%d.%m.%Y")

        assert row1_data[3].cget("text") == "Karlskrona"
        assert row1_data[4].cget("text") == "5.0°C"
        assert row2_data[3].cget("text") == "Stockholm"
        assert row2_data[4].cget("text") == "10.0°C"


class TestStartdateDisabled:
    def test_startdate_enabled_before_submit(self, app):
        """Start date picker should be enabled before any submission."""
        assert str(app.startdatepicker.cget("state")) != "disabled"

    @patch("src.weather_app.get_weather")
    def test_startdate_disabled_after_submit(self, mock_get_weather, app):
        """Start date picker should be disabled after the first submission."""
        mock_get_weather.return_value = [
            {
                "date": datetime.date.today().isoformat(),
                "max_temp": 10.0,
                "min_temp": 3.0,
                "condition": "Clear sky",
            },
        ]

        app.city_input.delete(0, tk.END)
        app.city_input.insert(0, "Karlskrona")
        app.duration_input.delete(0, tk.END)
        app.duration_input.insert(0, "1")
        app.startdatepicker.set_date(datetime.date.today())

        app.get_data()

        assert str(app.startdatepicker.cget("state")) == "disabled"


class TestMaxForecastDays:
    MAX_DAYS = 14

    def _make_mock_forecast(self, days):
        today = datetime.date.today()
        return [
            {
                "date": (today + datetime.timedelta(days=i)).isoformat(),
                "max_temp": 10.0 + i,
                "min_temp": 3.0,
                "condition": "Clear sky",
            }
            for i in range(days)
        ]

    def _submit_city(self, app, city, duration):
        app.city_input.delete(0, tk.END)
        app.city_input.insert(0, city)
        app.duration_input.delete(0, tk.END)
        app.duration_input.insert(0, str(duration))
        app.startdatepicker.set_date(datetime.date.today())
        app.get_data()

    @patch("src.weather_app.get_weather")
    def test_inputs_disabled_at_14_days(self, mock_get_weather, app):
        """Submit button, city input, and duration input are disabled after 14 days are filled."""
        mock_get_weather.return_value = self._make_mock_forecast(14)
        self._submit_city(app, "Karlskrona", 14)

        assert len(app.trip) == 14
        assert str(app.submit_btn.cget("state")) == "disabled"
        assert str(app.city_input.cget("state")) == "disabled"
        assert str(app.duration_input.cget("state")) == "disabled"

    @patch("src.weather_app.get_weather")
    def test_spinbox_max_updates_after_submit(self, mock_get_weather, app):
        """Duration spinbox max should reflect remaining days after a submission."""
        mock_get_weather.return_value = self._make_mock_forecast(5)
        self._submit_city(app, "Karlskrona", 5)

        assert len(app.trip) == 5
        assert int(float(app.duration_input.cget("to"))) == 9

    @patch("src.weather_app.get_weather")
    def test_reject_duration_exceeding_remaining(self, mock_get_weather, app):
        """Adding a city whose duration would exceed 14 total days should raise an error."""
        mock_get_weather.return_value = self._make_mock_forecast(10)
        self._submit_city(app, "Stockholm", 10)

        assert len(app.trip) == 10

        with patch("tkinter.messagebox.showerror"):
            with pytest.raises(ValueError):
                self._submit_city(app, "Gothenburg", 5)

        # Trip length should not have changed
        assert len(app.trip) == 10
