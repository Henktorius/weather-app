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
