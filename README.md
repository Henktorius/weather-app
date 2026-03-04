# Weather App

Desktop application for tracking weather on multiple cities on specific dates during a trip.

Developed as final project for the Software Testing course at BTH.

## Dependencies

The project relies on a set of external libraries that provide the following functionality:

- GUI: tkinter
- Unit testing: pytest
- Mocking API: pytest-mock
- External API: requests

## Development environment

We will use the Git CLI as the version control software and GitHub as the remote repository.

## CI Environment

To implement a continuous integration environment we will use GitHub Actions, which will run our tests every time someone pushes a commit to the repository.

## Requirements

1. Trip Configuration (Main Page)

- REQ-1.1: The app shall allow users to add multiple cities with a number of days representing how long the user will stay there to a trip list.
- REQ-1.2: The trip should have a start date
- REQ-1.3 (Constraints): The total duration of the trip shall not exceed 14 days.
- REQ-1.4: The user shall be able to remove a city from the list before searching.

2. Weather Data Integration

- REQ-2.1: The app shall fetch weather data for each city and its specific date range using the Open-Meteo API.
- REQ-2.2 (Missing Data): If the API returns no data for a specific date (e.g., too far in the future or past), the app shall display "Data Unavailable" for that day but continue to show data for other valid days.
- REQ-2.3: Data to be retrieved: City Name, Date, Max Temperature (Degrees), and Weather Condition (e.g., Sunny, Rainy).

3. Display & Visualization (Results Page)

- REQ-3.1: Results shall be displayed in a grid or scrollable list of "Weather Squares."
- REQ-3.2: Each square must contain: Date, City Name, Temperature, and a Short Description.
- REQ-3.3: The results page shall include a "Back" button to return to the Trip Configuration page.