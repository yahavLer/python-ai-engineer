"""
Mini-Project 1: Weather API Client
Fetches and processes weather data using the free Open-Meteo API.
"""

import requests
import json
from typing import Dict, Tuple, Optional
from datetime import datetime


# Common city coordinates (latitude, longitude)
CITY_COORDINATES = {
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "paris": (48.8566, 2.3522),
    "sydney": (33.8688, 151.2093),
    "toronto": (43.6532, -79.3832),
    "berlin": (52.5200, 13.4050),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "mumbai": (19.0760, 72.8777),
}


def get_coordinates(city: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude for a city.
    
    Args:
        city: City name (case-insensitive)
        
    Returns:
        Tuple of (latitude, longitude) or None if city not found
    """
    city_lower = city.lower().strip()
    if city_lower in CITY_COORDINATES:
        return CITY_COORDINATES[city_lower]
    return None


def fetch_weather(latitude: float, longitude: float, city_name: str = "Location") -> Optional[Dict]:
    """
    Fetch weather data from Open-Meteo API.
    
    Args:
        latitude: City latitude
        longitude: City longitude
        city_name: Name of the city for display
        
    Returns:
        Dictionary with weather data or None if request failed
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "auto"
    }
    
    try:
        print(f"🌐 Fetching weather data for {city_name}...")
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            "city": city_name,
            "latitude": latitude,
            "longitude": longitude,
            "current": data.get("current", {}),
            "timezone": data.get("timezone", "Unknown")
        }
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Unable to connect to the API")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout error: API request took too long")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("❌ Error parsing JSON response")
        return None


def format_weather_display(weather_data: Dict) -> str:
    """
    Format weather data for display.
    
    Args:
        weather_data: Dictionary containing weather information
        
    Returns:
        Formatted string for display
    """
    if not weather_data:
        return ""
    
    city = weather_data.get("city", "Unknown")
    timezone = weather_data.get("timezone", "Unknown")
    current = weather_data.get("current", {})
    
    temperature = current.get("temperature_2m", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind_speed = current.get("wind_speed_10m", "N/A")
    
    display = f"""
╔════════════════════════════════════════╗
║         🌤️  WEATHER REPORT  🌤️          ║
╚════════════════════════════════════════╝

📍 Location: {city}
🕐 Timezone: {timezone}
📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️  Temperature: {temperature}°C
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} km/h
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return display


def get_weather_recommendation(temperature: float, humidity: float) -> str:
    """
    Provide weather-based recommendations.
    
    Args:
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        
    Returns:
        Recommendation string
    """
    recommendations = []
    
    if temperature < 0:
        recommendations.append("❄️  Extremely cold - Wear heavy winter clothing!")
    elif temperature < 10:
        recommendations.append("🧥 Cold - Wear a warm jacket")
    elif temperature < 20:
        recommendations.append("🧤 Cool - Consider a light jacket")
    elif temperature < 25:
        recommendations.append("👕 Pleasant - Light clothing recommended")
    else:
        recommendations.append("☀️  Hot - Stay hydrated and wear sunscreen")
    
    if humidity > 80:
        recommendations.append("💦 High humidity - May feel muggy")
    elif humidity < 30:
        recommendations.append("🏜️  Low humidity - Use moisturizer")
    
    return "\n".join(recommendations)


def main():
    """Main function to run the weather client."""
    print("\n" + "="*50)
    print("     WEATHER API CLIENT (Open-Meteo)")
    print("="*50 + "\n")
    
    # Example 1: Fetch weather for a predefined city
    city = "London"
    coords = get_coordinates(city)
    
    if coords:
        latitude, longitude = coords
        weather_data = fetch_weather(latitude, longitude, city)
        
        if weather_data:
            print(format_weather_display(weather_data))
            
            # Get recommendations
            temperature = weather_data["current"].get("temperature_2m", 0)
            humidity = weather_data["current"].get("relative_humidity_2m", 0)
            recommendations = get_weather_recommendation(temperature, humidity)
            
            print("📋 Recommendations:")
            print(recommendations)
    else:
        print(f"❌ City '{city}' not found in available cities")
    
    # Example 2: Custom coordinates
    print("\n" + "-"*50 + "\n")
    print("📍 Fetching weather for custom coordinates (San Francisco)...")
    san_francisco_coords = (37.7749, -122.4194)
    weather_data_sf = fetch_weather(san_francisco_coords[0], san_francisco_coords[1], "San Francisco")
    
    if weather_data_sf:
        print(format_weather_display(weather_data_sf))
        temperature = weather_data_sf["current"].get("temperature_2m", 0)
        humidity = weather_data_sf["current"].get("relative_humidity_2m", 0)
        print("📋 Recommendations:")
        print(get_weather_recommendation(temperature, humidity))


if __name__ == "__main__":
    main()
