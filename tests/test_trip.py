from src.weather_app import Trip
import datetime


def test_trip_initialization():
    """Test that a Trip object initializes correctly."""
    start_date = datetime.date(2024, 1, 1)
    trip = Trip(start_date)
    assert trip.startdate == start_date
    assert trip.days == []


def test_add_day():
    """Test that adding a day to the trip works correctly."""
    trip = Trip(datetime.date(2024, 1, 1))
    trip.add_day(("2024-01-01", "20.5°C", "10ºC", "Clear sky"))
    assert len(trip.days) == 1
    assert trip.days[0] == ("2024-01-01", "20.5°C", "10ºC", "Clear sky")


def test_update_startdate():
    """Test that updating the start date of the trip works correctly."""
    trip = Trip(datetime.date(2024, 1, 1))
    new_date = datetime.date(2024, 2, 1)
    trip.update_startdate(new_date)
    assert trip.startdate == new_date
