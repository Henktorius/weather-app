import tkinter as tk
import datetime


def test_days_input(app):
    app.root.update()
    duration = app.root.nametowidget("duration_entry")
    duration.delete(0, tk.END)
    duration.insert(0, 10)
    assert int(duration.get()) == 10

def test_city_input(app):
    app.root.update()
    city = app.root.nametowidget("city_entry")
    city.delete(0, tk.END)
    city.insert(0, "London")
    assert city.get() == "London"

def test_date_input(app):
    app.root.update()
    date = app.startdatepicker
    date.set_date(datetime.date(2026, 3, 10))
    assert date.get_date() == datetime.date(2026, 3, 10)
