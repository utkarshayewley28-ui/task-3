import requests

# Ask the user for a city
city = input("Enter city name: ")

# Step 1: Find the city's latitude and longitude
geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_params = {
    "name": city,
    "count": 1,
    "language": "en",
    "format": "json"
}

try:
    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    # Check if the city was found
    if "results" not in geo_data:
        print("City not found. Please try again.")
    else:
        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Step 2: Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "temperature_unit": "celsius"
        }

        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()

        # Extract current weather data
        current = weather_data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        weather_code = current["weather_code"]

        # Convert weather code into a description
        weather_conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Heavy drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Light snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Light rain showers",
            81: "Moderate rain showers",
            82: "Heavy rain showers",
            95: "Thunderstorm"
        }

        condition = weather_conditions.get(
            weather_code,
            "Unknown weather condition"
        )

        # Display the weather
        print("\n----------------------------")
        print("       CURRENT WEATHER")
        print("----------------------------")
        print(f"City: {city_name}, {country}")
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {condition}")
        print("----------------------------")

except requests.exceptions.RequestException:
    print("Error: Could not connect to the weather API.")

except KeyError:
    print("Error: Weather data could not be read.")


