import datetime
import tkinter as tk
from tkinter import messagebox

from tkcalendar import DateEntry

from src.api_client import get_weather


class Trip:
    def __init__(self, startdate: datetime.date):
        self.startdate = startdate
        self.days = []

    def add_day(self, day: tuple[str, float]):
        self.days.append(day)

    def get_days(self):
        return self.days

    def __len__(self):
        return len(self.days)

    def update_startdate(self, new_date: datetime.date):
        self.startdate = new_date


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather")
        self.root.geometry("800x600")

        self.trip = Trip(datetime.date.today())

        self.label = tk.Label(root, text="Enter Startdate:", name="startdate_label")
        self.label.pack()
        self.startdatepicker = DateEntry(root, name="startdate_entry")
        self.startdatepicker.pack()

        self.label = tk.Label(root, text="Enter City:", name="cityinput_label")
        self.label.pack()

        self.city_input = tk.Entry(root, name="city_entry")
        self.city_input.pack()

        self.duration_label = tk.Label(
            root, text="Enter duration:", name="duration_label"
        )
        self.duration_label.pack()

        self.duration_input = tk.Spinbox(
            root, from_=1, to=14, increment=1, name="duration_entry"
        )
        self.duration_input.pack()

        self.submit_btn = tk.Button(
            root, text="Add City", command=self.get_data, name="submit_btn"
        )
        self.submit_btn.pack()

        self.forecast_container = tk.Frame(root, name="forecast_container")
        self.forecast_container.pack(padx=20, pady=10, fill="x")

    def get_data(self):
        if (
            self.startdatepicker.get_date() is None
            or self.startdatepicker.get_date() < datetime.date.today()
        ):
            messagebox.showerror("Error", "Please select a valid startdate")
            raise ValueError("Please select a valid startdate")

        if self.city_input.get() == "" or not self.city_input.get().isalpha():
            messagebox.showerror("Error", "Please enter a city")
            raise ValueError("Please enter a city")

        if (
            self.duration_input.get() == ""
            or not self.duration_input.get().isnumeric()
            or int(self.duration_input.get()) <= 0
            or int(self.duration_input.get()) > 14
        ):
            messagebox.showerror("Error", "Please enter a valid duration")
            raise ValueError("Please enter a valid duration")

        city = self.city_input.get()
        duration = int(self.duration_input.get())
        start_date = self.startdatepicker.get_date()
        first_day = start_date + datetime.timedelta(days=len(self.trip))
        last_day = first_day + datetime.timedelta(days=duration - 1)
        forecast = get_weather(city, first_day, last_day)

        # fill datastructure
        for day_data in forecast:
            temp_str = (
                f"{day_data['max_temp']}°C"
                if day_data["max_temp"] is not None
                else "N/A"
            )
            self.trip.add_day((f"{city}", temp_str))

        for days in self.trip.days[-int(duration) :]:
            self.add_forecast_row(days[0], days[1])

    def add_forecast_row(self, city, temp):
        row = tk.Frame(self.forecast_container, relief="groove", borderwidth=1)
        row.pack(fill="x", pady=2)

        row_num = len(self.forecast_container.winfo_children())
        tk.Label(row, text=f"#{row_num}", width=5, anchor="w").grid(
            row=0, column=0, padx=5
        )

        display_date = self.trip.startdate + datetime.timedelta(days=row_num - 1)
        day_of_week = display_date.strftime("%A")

        tk.Label(row, text=day_of_week, width=15, anchor="w").grid(
            row=0, column=1, padx=5
        )

        tk.Label(
            row, text=display_date.strftime("%d.%m.%Y"), width=20, anchor="w"
        ).grid(row=0, column=2, padx=5)

        tk.Label(row, text=city, width=20, anchor="w").grid(row=0, column=3, padx=5)
        tk.Label(row, text=temp, width=15).grid(row=0, column=4, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
