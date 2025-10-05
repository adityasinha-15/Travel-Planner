import os
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from typing import Dict, Any
import json

class WeatherService:
    def __init__(self):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    async def get_weather(self, location: str, dates: str, duration: int) -> Dict[str, Any]:
        """Get weather forecast for the trip dates using Open-Meteo API"""
        
        try:
            # Get coordinates for the location
            coordinates = self._get_coordinates_for_city(location)
            if not coordinates:
                return self._get_mock_weather(location, dates, duration)
            
            lat, lon = coordinates
            
            # Open-Meteo API URL
            url = "https://api.open-meteo.com/v1/forecast"
            
            # Parameters for current weather and daily forecast
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"],
                "daily": [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "temperature_2m_mean",
                    "relative_humidity_2m_mean",
                    "wind_speed_10m_max"
                ],
                "timezone": "auto",
                "forecast_days": min(duration, 16)  # Open-Meteo supports up to 16 days
            }
            
            # Make the API request
            responses = self.openmeteo.weather_api(url, params=params)
            response = responses[0]
            
            # Process current weather
            current = response.Current()
            current_weather = {
                "temperature": round(current.Variables(0).Value()),
                "feels_like": round(current.Variables(0).Value()),  # Open-Meteo doesn't provide feels_like
                "humidity": round(current.Variables(1).Value()),
                "wind_speed": round(current.Variables(2).Value()),
                "weather_code": current.Variables(3).Value()
            }
            
            # Process daily forecast
            daily = response.Daily()
            daily_weather_code = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_max = daily.Variables(1).ValuesAsNumpy()
            daily_temperature_min = daily.Variables(2).ValuesAsNumpy()
            daily_temperature_mean = daily.Variables(3).ValuesAsNumpy()
            daily_relative_humidity = daily.Variables(4).ValuesAsNumpy()
            daily_wind_speed = daily.Variables(5).ValuesAsNumpy()
            
            # Create date range
            daily_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                )
            }
            
            # Process forecast data
            forecast = []
            for i in range(min(duration, len(daily_data["date"]))):
                daily_forecast = {
                    "date": daily_data["date"][i].strftime("%Y-%m-%d"),
                    "min_temp": round(daily_temperature_min[i]),
                    "max_temp": round(daily_temperature_max[i]),
                    "avg_temp": round(daily_temperature_mean[i]),
                    "humidity": round(daily_relative_humidity[i]),
                    "wind_speed": round(daily_wind_speed[i]),
                    "weather_code": int(daily_weather_code[i]),
                    "description": self._weather_code_to_description(int(daily_weather_code[i]))
                }
                forecast.append(daily_forecast)
            
            # Create weather info
            weather_info = {
                "location": location,
                "current": {
                    "temperature": current_weather["temperature"],
                    "feels_like": current_weather["feels_like"],
                    "description": self._weather_code_to_description(int(current_weather["weather_code"])),
                    "humidity": current_weather["humidity"],
                    "wind_speed": current_weather["wind_speed"],
                    "icon": self._weather_code_to_icon(int(current_weather["weather_code"]))
                },
                "forecast": forecast,
                "recommendations": self._generate_recommendations(forecast)
            }
            
            return weather_info
            
        except Exception as e:
            print(f"Error fetching weather from Open-Meteo: {e}")
            return self._get_mock_weather(location, dates, duration)

    def _get_coordinates_for_city(self, location: str) -> tuple:
        """Get coordinates for major cities"""
        
        city_coordinates = {
            "rome": (41.9028, 12.4964),
            "paris": (48.8566, 2.3522),
            "london": (51.5074, -0.1278),
            "tokyo": (35.6762, 139.6503),
            "barcelona": (41.3851, 2.1734),
            "new york": (40.7128, -74.0060),
            "berlin": (52.5200, 13.4050),
            "madrid": (40.4168, -3.7038),
            "amsterdam": (52.3676, 4.9041),
            "sydney": (-33.8688, 151.2093),
            "dubai": (25.2048, 55.2708),
            "singapore": (1.3521, 103.8198),
            "mumbai": (19.0760, 72.8777),
            "moscow": (55.7558, 37.6176),
            "istanbul": (41.0082, 28.9784)
        }
        
        location_lower = location.lower()
        for city, coords in city_coordinates.items():
            if city in location_lower:
                return coords
        
        # Default to Rome if not found
        return (41.9028, 12.4964)

    def _weather_code_to_description(self, code: int) -> str:
        """Convert WMO weather code to description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown")

    def _weather_code_to_icon(self, code: int) -> str:
        """Convert WMO weather code to icon identifier"""
        if code in [0, 1]:
            return "01d"  # Clear sky
        elif code in [2, 3]:
            return "02d"  # Partly cloudy
        elif code in [45, 48]:
            return "50d"  # Fog
        elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "10d"  # Rain
        elif code in [71, 73, 75, 77, 85, 86]:
            return "13d"  # Snow
        elif code in [95, 96, 99]:
            return "11d"  # Thunderstorm
        else:
            return "02d"  # Default

    def _generate_recommendations(self, forecast: list) -> list:
        """Generate weather-based recommendations"""
        
        recommendations = []
        
        for day in forecast:
            temp = day["avg_temp"]
            description = day["description"].lower()
            
            if "rain" in description or "drizzle" in description or "shower" in description:
                recommendations.append(f"Pack an umbrella for {day['date']} - {description}")
            elif "thunderstorm" in description:
                recommendations.append(f"Stay indoors during thunderstorms on {day['date']} - {description}")
            elif "snow" in description:
                recommendations.append(f"Wear warm, waterproof clothing for {day['date']} - {description}")
            elif temp < 10:
                recommendations.append(f"Bring warm clothes for {day['date']} - temperature around {temp}°C")
            elif temp > 25:
                recommendations.append(f"Wear light, breathable clothing for {day['date']} - temperature around {temp}°C")
            elif "clear" in description or "sunny" in description:
                recommendations.append(f"Perfect weather for outdoor activities on {day['date']}")
            elif "fog" in description:
                recommendations.append(f"Be cautious when driving on {day['date']} due to fog")
        
        return recommendations

    def _get_mock_weather(self, location: str, dates: str, duration: int) -> Dict[str, Any]:
        """Return mock weather data when API is not available"""
        
        mock_forecast = []
        for i in range(min(duration, 5)):
            mock_forecast.append({
                "date": f"2024-{10+i:02d}-15",
                "min_temp": 15 + i,
                "max_temp": 22 + i,
                "avg_temp": 18 + i,
                "description": "Partly Cloudy",
                "icon": "02d",
                "humidity": 65,
                "wind_speed": 3.5
            })
        
        return {
            "location": location,
            "current": {
                "temperature": 20,
                "feels_like": 22,
                "description": "Partly Cloudy",
                "humidity": 65,
                "wind_speed": 3.5,
                "icon": "02d"
            },
            "forecast": mock_forecast,
            "recommendations": [
                f"Pleasant weather expected for your trip to {location}",
                "Pack layers for changing temperatures",
                "Bring comfortable walking shoes"
            ]
        }
