# Weather-Monitoring Project

## 1. What This Project is About

The `Weather Monitoring` project is a Python-based application that fetches and monitors real-time weather data for six major metro cities in India: Delhi, Mumbai, Chennai, Bengaluru, Kolkata, and Hyderabad. The project fetches weather data from the OpenWeatherMap API and stores it in a local SQLite database for analysis and visualization.

### Key Features:
- **Real-Time Weather Data:** Fetches the current weather details such as average temperature, minimum temperature, maximum temperature, and dominant weather condition for each city at a configurable interval of 5 minutes.
- **Alerts:** Generates alerts if the average temperature of any city exceeds a predefined threshold which is set to 35°C currently.
- **Data Storage:** Saves weather data into a local SQLite database for future retrieval and analysis.
- **Temperature Trend Visualization:** Plots the temperature trends for all cities over time using `matplotlib`.

---

## 2. Explaining Structure of the Python Code

The code is organized into several key functions that manage the database setup, data fetching, summary calculation, data storage, and trend plotting:

### Functions:
1. **`init_db(db_path)`**:
   - Initializes the SQLite database and creates a table (`weather_data`) to store weather information.
   
2. **`fetch_data_for_cities(api_key, cities)`**:
   - Fetches real-time weather data from the OpenWeatherMap API for the specified cities and returns the raw weather data.
   
3. **`calculate_daily_summary(raw_data, threshold=30)`**:
   - Processes the raw weather data and calculates daily summaries such as average temperature, min/max temperature, and dominant weather condition. It also generates alerts if temperatures exceed a given threshold (30°C by default).

4. **`save_summary(daily_summary, db_path)`**:
   - Saves the calculated daily weather summary into the SQLite database.

5. **`fetch_all_cities_data(db_path)`**:
   - Fetches all stored weather data for all cities from the SQLite database.

6. **`plot_all_cities_trends(db_path)`**:
   - Plots the temperature trends for all cities based on the stored data using `matplotlib`.

7. **`main(db_path)`**:
   - The main function that runs the weather monitoring process. It initializes the database, fetches weather data at regular intervals (every 5 minutes), and stores the data while also plotting temperature trends.

---

## 3. Required Libraries and Software

To run this project, you need the following libraries and software:

### Python Libraries:
1. **`sqlite3`** - Used for database management and storage of weather data.
   - Comes with Python by default, no need for additional installation.
   
2. **`requests`** - Used to make HTTP requests to the OpenWeatherMap API for fetching real-time weather data.
   - Install using:
     ```bash
     pip install requests
     ```

3. **`matplotlib`** - Used for plotting the temperature trends of different cities.
   - Install using:
     ```bash
     pip install matplotlib
     ```

4. **`datetime`** - Provides date and time utilities.
   - Comes with Python by default, no need for additional installation.

### Software:
- **Python** - Make sure Python is installed on your system (version 3.x recommended).
- **OpenWeatherMap API Key** - You'll need an API key from OpenWeatherMap to fetch real-time weather data. You can get one by signing up on their website [here](https://home.openweathermap.org/users/sign_up).

---

## How to Run the Project

1. **Install the required libraries** using the provided `pip install` commands.
2. **Set up the OpenWeatherMap API Key** in the code (`main` function) where `API_KEY` is defined.
3. **Clone the project source code** and name it as per your need with `.py` extension.
4. **Run the source code** script in your preferred Python IDE or through the terminal:
   ```bash
   python app.py

---
