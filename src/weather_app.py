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
        self.root.geometry("600x400")

        self.trip = Trip(datetime.date.today())

        self.label = tk.Label(root, text="Enter Startdate:", name="startdate_label")
        self.label.pack()
        self.startdatepicker = DateEntry(root, name="startdate_entry")
        self.startdatepicker.pack()

        self.label = tk.Label(root, text="Enter City:", name="cityinput_label")
        self.label.pack()

        self.city_input = tk.Entry(root, name="city_entry")
        self.city_input.pack()

        self.duration_label = tk.Label(root, text="Enter duration:", name="duration_label")
        self.duration_label.pack()

        self.duration_input = tk.Spinbox(root, from_=1, to=14, increment=1, name="duration_entry")
        self.duration_input.pack()

        self.submit_btn = tk.Button(root, text="Get Weather", command=self.update_label, name="submit_btn")
        self.submit_btn.pack()


    def update_label(self):
        city = self.city_input.get()
        if city:
            self.label.config(text=f"Weather for {city} on {self.trip.startdate}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
