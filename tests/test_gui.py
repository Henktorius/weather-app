import datetime


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
