import asyncio
from typing import Dict, Any
from .gemini_client import GeminiClient
from .hotels import HotelsService
from .weather import WeatherService
from .attractions import AttractionsService
from .flights import FlightsService
from .routes import RoutesService
import json

class TripPlanner:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.hotels_service = HotelsService()
        self.weather_service = WeatherService()
        self.attractions_service = AttractionsService()
        self.flights_service = FlightsService()
        self.routes_service = RoutesService()

    async def plan_trip(self, prompt: str) -> Dict[str, Any]:
        """Main method to plan a complete trip"""
        
        # Step 1: Analyze the prompt using Gemini
        trip_details = await self.gemini_client.analyze_prompt(prompt)
        
        destination = trip_details.get("destination", "Unknown")
        duration = trip_details.get("duration", 3)
        dates = trip_details.get("dates", "Not specified")
        budget = trip_details.get("budget", "moderate")
        interests = trip_details.get("interests", [])
        requirements = trip_details.get("requirements", [])
        
        # Step 2: Gather data from various APIs in parallel
        tasks = [
            self.hotels_service.search_hotels(destination, budget, requirements),
            self.attractions_service.get_attractions(destination, interests),
            self.weather_service.get_weather(destination, dates, duration),
            self.flights_service.get_flights("User Location", destination, dates),
            self.routes_service.get_sample_routes(destination)
        ]
        
        # Execute all API calls in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        hotels, attractions, weather, flights, routes = results
        
        # Handle any exceptions in API calls
        hotels = hotels if not isinstance(hotels, Exception) else []
        attractions = attractions if not isinstance(attractions, Exception) else []
        weather = weather if not isinstance(weather, Exception) else {}
        flights = flights if not isinstance(flights, Exception) else []
        routes = routes if not isinstance(routes, Exception) else []
        
        # Step 3: Generate comprehensive plan using Gemini
        tool_results = {
            "hotels": hotels,
            "attractions": attractions,
            "weather": weather,
            "flights": flights,
            "routes": routes,
            "trip_details": trip_details
        }
        
        summary = await self.gemini_client.plan_trip_with_tools(prompt, tool_results)
        
        return {
            "destination": destination,
            "duration": duration,
            "dates": dates,
            "hotels": hotels,
            "attractions": attractions,
            "weather": weather,
            "flights": flights,
            "routes": routes,
            "summary": summary
        }
