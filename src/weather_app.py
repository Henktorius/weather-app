import tkinter as tk
import datetime
from tkcalendar import DateEntry


class Trip:
    def __init__(self, startdate: datetime.date):
        self.startdate = startdate
        self.days = []

    def add_day(self, day: tuple[str, float]):
        self.days.append(day)

    def update_startdate(self, new_date: datetime.date):
        self.startdate = new_date


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather")

        self.trip = Trip(datetime.date.today())

        self.label = tk.Label(root, text="Enter Startdate:")
        self.label.pack()
        self.startdatepicker = DateEntry(root)
        self.startdatepicker.pack()


        self.label = tk.Label(root, text="Enter City:")
        self.label.pack()

        self.city_input = tk.Entry(root)
        self.city_input.pack()

        self.submit_btn = tk.Button(root, text="Get Weather", command=self.update_label)
        self.submit_btn.pack()

    def update_label(self):
        city = self.city_input.get()
        if city:
            self.label.config(text=f"Weather for {city} on {self.trip.startdate}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
