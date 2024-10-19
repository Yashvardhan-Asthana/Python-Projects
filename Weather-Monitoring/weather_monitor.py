import os
import sqlite3
import time
import requests
from datetime import datetime
import matplotlib.pyplot as plt

# Database setup
def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a table to store the weather data if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        avg_temp REAL,
        min_temp REAL,
        max_temp REAL,
        dominant_condition TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()
    print("Database initialized and table is ready (if it did not exist).")

# Fetch weather data for the given cities
def fetch_data_for_cities(api_key, cities):
    raw_data = {}
    for city in cities:
        print(f"\nFetching weather data for {city}...")
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        if response.status_code == 200:
            print("Data fetched Successfully")
            raw_data[city] = response.json() # raw data will return all the data of 5 cities
            # print(raw_data)
        else:
            print(f"Failed to fetch data for {city}: {response.status_code} {response.text}")
    return raw_data

# Calculate daily summary from raw data
def calculate_daily_summary(raw_data, threshold=30):
    daily_summary = {} # daily summary is the 5 data of 6 cities that we need
    
    for city, data in raw_data.items():
        avg_temp = data['main']['temp']
        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        condition = data['weather'][0]['main']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        
        alert = None
        if avg_temp > threshold:
            alert = f"Alert: Average temperature in {city} exceeds the threshold of {threshold}°C!"

        daily_summary[city] = {
            'avg_temp': avg_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'dominant_condition': condition,
            'timestamp': timestamp,
            'alert': alert
        }
   
    return daily_summary

# Saving summary to the database
def save_summary(daily_summary, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for city, summary in daily_summary.items():
        cursor.execute('''INSERT INTO weather_data (city, avg_temp, min_temp, max_temp, dominant_condition, timestamp)
                          VALUES (?, ?, ?, ?, ?, ?)''', 
                       (city, summary['avg_temp'], summary['min_temp'], summary['max_temp'], summary['dominant_condition'], summary['timestamp']))
        
        if summary['alert']:
            print(summary['alert'])  
    # print(daily_summary)
    print(f"\nInserted data for cities: {', '.join(daily_summary.keys())}")  # Debug output

    conn.commit()  # Ensure changes are committed
    conn.close()
    
# Fetch data for all cities from the database table
def fetch_all_cities_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT city, avg_temp, timestamp FROM weather_data
    ''')
    rows = cursor.fetchall()
    conn.close()

    return rows

# Function to plot temperature trends for all cities
def plot_all_cities_trends(db_path):
    data = fetch_all_cities_data(db_path)

    if data:
        city_data = {}

        # Organize data by city
        for row in data:
            city, avg_temp, timestamp = row
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if city not in city_data:
                city_data[city] = {'timestamps': [], 'temps': []}
            city_data[city]['timestamps'].append(timestamp)
            city_data[city]['temps'].append(avg_temp)

        # Plot temperature trends for each city
        plt.figure(figsize=(10, 6))
        for city, values in city_data.items():
            plt.plot(values['timestamps'], values['temps'], label=city)

        plt.xlabel('Timestamp')
        plt.ylabel('Average Temperature (°C)')
        plt.title('Temperature Trends for Different Cities')
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
    else:
        print("No data available to plot.")

    
# Main function
def main(db_path):
    # API Key and list of cities
    API_KEY = "7620e82642fc9a1c3882f2c4697ed2d0"
    CITIES = ["Delhi", "Mumbai", "Chennai", "Bengaluru", "Kolkata", "Hyderabad"]

    # Initialize database
    init_db(db_path)
    print(f"Database path: {db_path}")

    while True:
        # Fetch and process weather data
        raw_data = fetch_data_for_cities(API_KEY, CITIES)
        if raw_data:
            daily_summary = calculate_daily_summary(raw_data)
            save_summary(daily_summary, db_path)  # Save data immediately after fetching
            print("Weather data saved to the database.")
        else:
            print("No data fetched. Skipping this cycle.")
        
        # Wait for 5 seconds before fetching again
        time.sleep(5)  # Can be changed to 5 minutes or more
        
        # Plot the weather trends for all cities
        plot_all_cities_trends(db_path)

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), 'weather.db')

    # Initialize the database and fetch weather data
    main(db_path)
