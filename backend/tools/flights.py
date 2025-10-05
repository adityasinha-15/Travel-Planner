import os
import aiohttp
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta
import random

class FlightsService:
    def __init__(self):
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
        self.base_url = "https://test.api.amadeus.com/v2"

    async def get_flights(self, origin: str, destination: str, dates: str) -> List[Dict[str, Any]]:
        """Search for flights between origin and destination"""
        
        # For now, return mock data since Amadeus API requires complex setup
        # In production, you would implement actual Amadeus API calls here
        return self._get_mock_flights(origin, destination, dates)

    async def _search_amadeus_flights(self, origin: str, destination: str, departure_date: str, return_date: str = None) -> List[Dict[str, Any]]:
        """Search flights using Amadeus API (placeholder implementation)"""
        
        if not self.amadeus_api_key or not self.amadeus_api_secret:
            return self._get_mock_flights(origin, destination, departure_date)
        
        try:
            # First, get access token
            token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            token_data = {
                "grant_type": "client_credentials",
                "client_id": self.amadeus_api_key,
                "client_secret": self.amadeus_api_secret
            }
            
            async with aiohttp.ClientSession() as session:
                # Get access token
                async with session.post(token_url, data=token_data) as response:
                    if response.status == 200:
                        token_response = await response.json()
                        access_token = token_response["access_token"]
                    else:
                        return self._get_mock_flights(origin, destination, departure_date)
                
                # Search flights
                headers = {"Authorization": f"Bearer {access_token}"}
                search_url = f"{self.base_url}/shopping/flight-offers"
                
                params = {
                    "originLocationCode": self._get_airport_code(origin),
                    "destinationLocationCode": self._get_airport_code(destination),
                    "departureDate": departure_date,
                    "adults": 1,
                    "max": 10
                }
                
                if return_date:
                    params["returnDate"] = return_date
                
                async with session.get(search_url, headers=headers, params=params) as response:
                    if response.status == 200:
                        flight_data = await response.json()
                        return self._process_amadeus_flights(flight_data)
                    else:
                        return self._get_mock_flights(origin, destination, departure_date)
        
        except Exception as e:
            print(f"Error searching flights: {e}")
            return self._get_mock_flights(origin, destination, departure_date)

    def _get_airport_code(self, location: str) -> str:
        """Convert location name to airport code (simplified mapping)"""
        
        airport_codes = {
            "rome": "FCO",
            "paris": "CDG",
            "london": "LHR",
            "new york": "JFK",
            "tokyo": "NRT",
            "sydney": "SYD",
            "berlin": "TXL",
            "madrid": "MAD",
            "amsterdam": "AMS",
            "barcelona": "BCN"
        }
        
        location_lower = location.lower()
        for city, code in airport_codes.items():
            if city in location_lower:
                return code
        
        return "XXX"  # Default code

    def _process_amadeus_flights(self, flight_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process Amadeus API response into our format"""
        
        flights = []
        
        for offer in flight_data.get("data", [])[:10]:  # Limit to 10 flights
            
            flight = {
                "price": {
                    "total": float(offer["price"]["total"]),
                    "currency": offer["price"]["currency"]
                },
                "itineraries": [],
                "traveler_pricings": offer.get("travelerPricings", [])
            }
            
            for itinerary in offer["itineraries"]:
                itinerary_data = {
                    "duration": itinerary["duration"],
                    "segments": []
                }
                
                for segment in itinerary["segments"]:
                    segment_data = {
                        "departure": {
                            "airport": segment["departure"]["iataCode"],
                            "terminal": segment["departure"].get("terminal", ""),
                            "time": segment["departure"]["at"]
                        },
                        "arrival": {
                            "airport": segment["arrival"]["iataCode"],
                            "terminal": segment["arrival"].get("terminal", ""),
                            "time": segment["arrival"]["at"]
                        },
                        "carrier_code": segment["carrierCode"],
                        "flight_number": segment["number"],
                        "aircraft": segment.get("aircraft", {}).get("code", ""),
                        "duration": segment["duration"]
                    }
                    
                    itinerary_data["segments"].append(segment_data)
                
                flight["itineraries"].append(itinerary_data)
            
            flights.append(flight)
        
        return flights

    def _get_mock_flights(self, origin: str, destination: str, dates: str) -> List[Dict[str, Any]]:
        """Return mock flight data"""
        
        airlines = ["Air France", "Lufthansa", "British Airways", "Alitalia", "Ryanair", "EasyJet"]
        airports = {
            "rome": "FCO",
            "paris": "CDG", 
            "london": "LHR",
            "berlin": "TXL",
            "madrid": "MAD"
        }
        
        origin_code = airports.get(origin.lower(), "XXX")
        dest_code = airports.get(destination.lower(), "XXX")
        
        mock_flights = []
        
        for i in range(5):  # Generate 5 mock flights
            airline = random.choice(airlines)
            base_price = random.randint(200, 800)
            
            # Create departure and arrival times
            departure_hour = random.randint(6, 22)
            arrival_hour = (departure_hour + random.randint(2, 6)) % 24
            
            flight = {
                "price": {
                    "total": base_price,
                    "currency": "EUR"
                },
                "itineraries": [
                    {
                        "duration": f"PT{random.randint(2, 6)}H{random.randint(0, 59)}M",
                        "segments": [
                            {
                                "departure": {
                                    "airport": origin_code,
                                    "terminal": random.choice(["1", "2", "3", ""]),
                                    "time": f"2024-10-15T{departure_hour:02d}:{random.randint(0, 59):02d}:00"
                                },
                                "arrival": {
                                    "airport": dest_code,
                                    "terminal": random.choice(["1", "2", "3", ""]),
                                    "time": f"2024-10-15T{arrival_hour:02d}:{random.randint(0, 59):02d}:00"
                                },
                                "carrier_code": airline[:2].upper(),
                                "flight_number": f"{random.randint(100, 9999)}",
                                "aircraft": random.choice(["320", "737", "787", "A380"]),
                                "duration": f"PT{random.randint(2, 6)}H{random.randint(0, 59)}M"
                            }
                        ]
                    }
                ],
                "traveler_pricings": [
                    {
                        "traveler_id": "1",
                        "fare_option": "STANDARD",
                        "traveler_type": "ADULT",
                        "price": {
                            "currency": "EUR",
                            "total": str(base_price),
                            "base": str(base_price - 50)
                        }
                    }
                ],
                "airline": airline,
                "stops": random.choice([0, 1, 2]),
                "duration_hours": random.randint(2, 8)
            }
            
            mock_flights.append(flight)
        
        # Sort by price
        return sorted(mock_flights, key=lambda x: x["price"]["total"])

    def _format_flight_summary(self, flight: Dict[str, Any]) -> str:
        """Format flight information for display"""
        
        if not flight.get("itineraries"):
            return "No flight details available"
        
        itinerary = flight["itineraries"][0]
        segments = itinerary["segments"]
        
        if not segments:
            return "No flight segments available"
        
        first_segment = segments[0]
        last_segment = segments[-1]
        
        departure = first_segment["departure"]
        arrival = last_segment["arrival"]
        
        return f"{departure['airport']} → {arrival['airport']} | {flight['price']['currency']} {flight['price']['total']}"
