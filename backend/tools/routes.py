import os
import googlemaps
from typing import List, Dict, Any
import json

class RoutesService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if api_key:
            self.gmaps = googlemaps.Client(key=api_key)
        else:
            self.gmaps = None

    async def get_routes(self, start_location: str, end_location: str, waypoints: List[str] = None) -> Dict[str, Any]:
        """Get optimized route between locations with optional waypoints"""
        
        if not self.gmaps:
            return self._get_mock_route(start_location, end_location, waypoints)
        
        try:
            # Prepare waypoints for Google Directions API
            waypoints_str = "|".join(waypoints) if waypoints else None
            
            # Get directions
            directions_result = self.gmaps.directions(
                origin=start_location,
                destination=end_location,
                waypoints=waypoints_str,
                mode="driving",
                optimize_waypoints=True if waypoints else False,
                alternatives=False
            )
            
            if not directions_result:
                return self._get_mock_route(start_location, end_location, waypoints)
            
            route = directions_result[0]
            
            # Process route data
            route_info = {
                "start_location": start_location,
                "end_location": end_location,
                "waypoints": waypoints or [],
                "total_distance": route["legs"][0]["distance"]["text"],
                "total_duration": route["legs"][0]["duration"]["text"],
                "overview_polyline": route["overview_polyline"]["points"],
                "legs": [],
                "steps": []
            }
            
            # Process each leg of the journey
            for leg in route["legs"]:
                leg_info = {
                    "start_address": leg["start_address"],
                    "end_address": leg["end_address"],
                    "distance": leg["distance"]["text"],
                    "duration": leg["duration"]["text"],
                    "steps": []
                }
                
                for step in leg["steps"]:
                    step_info = {
                        "instruction": step["html_instructions"],
                        "distance": step["distance"]["text"],
                        "duration": step["duration"]["text"],
                        "start_location": step["start_location"],
                        "end_location": step["end_location"],
                        "travel_mode": step["travel_mode"]
                    }
                    
                    leg_info["steps"].append(step_info)
                
                route_info["legs"].append(leg_info)
            
            return route_info
            
        except Exception as e:
            print(f"Error getting routes: {e}")
            return self._get_mock_route(start_location, end_location, waypoints)

    async def get_sample_routes(self, destination: str) -> List[Dict[str, Any]]:
        """Get sample routes for popular attractions in a destination"""
        
        if not self.gmaps:
            return self._get_mock_sample_routes(destination)
        
        try:
            # Define sample attractions for different cities
            sample_attractions = self._get_sample_attractions(destination)
            
            if not sample_attractions:
                return self._get_mock_sample_routes(destination)
            
            routes = []
            
            # Create routes between different attractions
            for i in range(min(3, len(sample_attractions))):
                start_attraction = sample_attractions[i]
                
                for j in range(i + 1, min(i + 3, len(sample_attractions))):
                    end_attraction = sample_attractions[j]
                    
                    route = await self.get_routes(
                        start_attraction["location"],
                        end_attraction["location"]
                    )
                    
                    if route:
                        route["start_attraction"] = start_attraction["name"]
                        route["end_attraction"] = end_attraction["name"]
                        route["route_type"] = "attraction_to_attraction"
                        routes.append(route)
            
            return routes
            
        except Exception as e:
            print(f"Error getting sample routes: {e}")
            return self._get_mock_sample_routes(destination)

    def _get_sample_attractions(self, destination: str) -> List[Dict[str, str]]:
        """Get sample attractions for a destination"""
        
        attraction_map = {
            "rome": [
                {"name": "Colosseum", "location": "Colosseum, Rome, Italy"},
                {"name": "Vatican City", "location": "Vatican City"},
                {"name": "Trevi Fountain", "location": "Trevi Fountain, Rome, Italy"},
                {"name": "Roman Forum", "location": "Roman Forum, Rome, Italy"}
            ],
            "paris": [
                {"name": "Eiffel Tower", "location": "Eiffel Tower, Paris, France"},
                {"name": "Louvre Museum", "location": "Louvre Museum, Paris, France"},
                {"name": "Notre-Dame", "location": "Notre-Dame Cathedral, Paris, France"},
                {"name": "Arc de Triomphe", "location": "Arc de Triomphe, Paris, France"}
            ],
            "london": [
                {"name": "Big Ben", "location": "Big Ben, London, UK"},
                {"name": "Tower Bridge", "location": "Tower Bridge, London, UK"},
                {"name": "British Museum", "location": "British Museum, London, UK"},
                {"name": "Buckingham Palace", "location": "Buckingham Palace, London, UK"}
            ],
            "new york": [
                {"name": "Statue of Liberty", "location": "Statue of Liberty, New York, USA"},
                {"name": "Times Square", "location": "Times Square, New York, USA"},
                {"name": "Central Park", "location": "Central Park, New York, USA"},
                {"name": "Brooklyn Bridge", "location": "Brooklyn Bridge, New York, USA"}
            ]
        }
        
        # Find matching destination
        destination_lower = destination.lower()
        for city, attractions in attraction_map.items():
            if city in destination_lower:
                return attractions
        
        # Default attractions
        return [
            {"name": f"Main Square", "location": f"City Center, {destination}"},
            {"name": f"Central Museum", "location": f"Museum District, {destination}"},
            {"name": f"Historic District", "location": f"Old Town, {destination}"}
        ]

    def _get_mock_route(self, start_location: str, end_location: str, waypoints: List[str] = None) -> Dict[str, Any]:
        """Return mock route data"""
        
        return {
            "start_location": start_location,
            "end_location": end_location,
            "waypoints": waypoints or [],
            "total_distance": "5.2 km",
            "total_duration": "15 mins",
            "overview_polyline": "mock_polyline_data",
            "legs": [
                {
                    "start_address": start_location,
                    "end_address": end_location,
                    "distance": "5.2 km",
                    "duration": "15 mins",
                    "steps": [
                        {
                            "instruction": f"Head toward {end_location}",
                            "distance": "5.2 km",
                            "duration": "15 mins",
                            "start_location": {"lat": 41.9028, "lng": 12.4964},
                            "end_location": {"lat": 41.9028, "lng": 12.4964},
                            "travel_mode": "DRIVING"
                        }
                    ]
                }
            ],
            "steps": []
        }

    def _get_mock_sample_routes(self, destination: str) -> List[Dict[str, Any]]:
        """Return mock sample routes"""
        
        sample_attractions = self._get_sample_attractions(destination)
        
        routes = []
        for i in range(min(2, len(sample_attractions) - 1)):
            route = self._get_mock_route(
                sample_attractions[i]["location"],
                sample_attractions[i + 1]["location"]
            )
            route["start_attraction"] = sample_attractions[i]["name"]
            route["end_attraction"] = sample_attractions[i + 1]["name"]
            route["route_type"] = "attraction_to_attraction"
            routes.append(route)
        
        return routes

    def create_optimized_itinerary(self, attractions: List[Dict[str, Any]], hotel_location: str) -> Dict[str, Any]:
        """Create an optimized daily itinerary based on attractions and hotel location"""
        
        if not attractions:
            return {"error": "No attractions provided"}
        
        itinerary = {
            "day_plans": [],
            "total_distance": "0 km",
            "estimated_total_time": "0 hours"
        }
        
        # Simple itinerary creation (in production, you'd use more sophisticated algorithms)
        daily_attractions = attractions[:6]  # Limit to 6 attractions per day
        
        day_plan = {
            "day": 1,
            "attractions": daily_attractions,
            "start_location": hotel_location,
            "end_location": hotel_location,
            "estimated_duration": "8 hours",
            "estimated_distance": "12 km"
        }
        
        itinerary["day_plans"].append(day_plan)
        itinerary["total_distance"] = day_plan["estimated_distance"]
        itinerary["estimated_total_time"] = day_plan["estimated_duration"]
        
        return itinerary
