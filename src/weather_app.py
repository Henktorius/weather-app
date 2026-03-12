import datetime
import tkinter as tk
from tkinter import messagebox

from tkcalendar import DateEntry

try:
    from src.api_client import get_weather
except ImportError:
    from api_client import get_weather


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
    HEADER_COLUMNS = [
        ("Day", 5),
        ("", 15),
        ("Date", 15),
        ("City", 15),
        ("Temperature", 15),
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Travel Weather")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")

        self.trip = Trip(datetime.date.today())
        self.forecast_row_count = 0

        self._create_input_widgets()
        self._create_forecast_container()

    def _create_input_widgets(self):
        root = self.root
        pad = dict(padx=10, pady=10, sticky="w")

        # Row 0: Start date
        tk.Label(
            root, text="Trip Startdate:", name="startdate_label", bg="lightblue"
        ).grid(row=0, column=0, **pad)
        self.startdatepicker = DateEntry(root, name="startdate_entry")
        self.startdatepicker.grid(row=0, column=1, **pad)

        # Row 1: City
        tk.Label(root, text="Enter City:", name="cityinput_label", bg="lightblue").grid(
            row=1, column=0, **pad
        )
        self.city_input = tk.Entry(root, name="city_entry")
        self.city_input.grid(row=1, column=1, **pad)

        # Row 2: Duration + submit
        tk.Label(
            root, text="Duration of the City:", name="duration_label", bg="lightblue"
        ).grid(row=2, column=0, **pad)
        self.duration_input = tk.Spinbox(
            root, from_=1, to=14, increment=1, name="duration_entry"
        )
        self.duration_input.grid(row=2, column=1, **pad)

        self.submit_btn = tk.Button(
            root, text="Add City", command=self.get_data, name="submit_btn"
        )
        self.submit_btn.grid(row=2, column=3, **pad)

    def _create_forecast_container(self):
        self.forecast_container = tk.Frame(self.root, name="forecast_container")
        self.forecast_container.grid(
            row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew"
        )

        header = tk.Frame(self.forecast_container, relief="groove", borderwidth=1)
        header.pack(fill="x", pady=2)
        for col, (text, width) in enumerate(self.HEADER_COLUMNS):
            tk.Label(header, text=text, width=width, anchor="w").grid(
                row=0, column=col, padx=5
            )

    def _validate_inputs(self):
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

        remaining = 14 - len(self.trip)
        if int(self.duration_input.get()) > remaining:
            messagebox.showerror(
                "Error",
                f"Maximum 14 forecast days allowed. You can add up to {remaining} more day(s).",
            )
            raise ValueError("Exceeds 14-day forecast limit")

    def get_data(self):
        self._validate_inputs()

        city = self.city_input.get()
        duration = int(self.duration_input.get())
        start_date = self.startdatepicker.get_date()
        first_day = start_date + datetime.timedelta(days=len(self.trip))
        last_day = first_day + datetime.timedelta(days=duration - 1)
        forecast = get_weather(city, first_day, last_day)

        # fill datastructure
        for day_data in forecast:
            max_temp = day_data["max_temp"]
            temp_str = f"{max_temp}°C" if max_temp is not None else "N/A"
            self.trip.add_day((city, temp_str))

        for city_name, temp_val in self.trip.days[-duration:]:
            self._add_forecast_row(city_name, temp_val)

        self.startdatepicker.configure(state="disabled")

        remaining = 14 - len(self.trip)
        if remaining <= 0:
            self.submit_btn.configure(state="disabled")
            self.city_input.configure(state="disabled")
            self.duration_input.configure(state="disabled")
        else:
            self.duration_input.configure(to=remaining)

    def _add_forecast_row(self, city, temp):
        row = tk.Frame(self.forecast_container, relief="groove", borderwidth=1)
        row.pack(fill="x", pady=2)

        self.forecast_row_count += 1
        row_num = self.forecast_row_count
        display_date = self.trip.startdate + datetime.timedelta(days=row_num - 1)

        columns = [
            (f"#{row_num}", 5),
            (display_date.strftime("%A"), 15),
            (display_date.strftime("%d.%m.%Y"), 15),
            (city, 15),
            (temp, 15),
        ]
        for col, (text, width) in enumerate(columns):
            tk.Label(row, text=text, width=width, anchor="w").grid(
                row=0, column=col, padx=5
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
