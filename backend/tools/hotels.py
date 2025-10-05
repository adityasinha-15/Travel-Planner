import os
import googlemaps
from typing import List, Dict, Any
import json

class HotelsService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if api_key:
            self.gmaps = googlemaps.Client(key=api_key)
        else:
            self.gmaps = None

    async def search_hotels(self, location: str, budget: str = "moderate", requirements: List[str] = None) -> List[Dict[str, Any]]:
        """Search for hotels using Google Places API"""
        
        if not self.gmaps:
            # Return mock data if API key not available
            return self._get_mock_hotels(location, budget)
        
        try:
            # Search for hotels near the location
            places_result = self.gmaps.places_nearby(
                location=location,
                radius=5000,  # 5km radius
                type='lodging'
            )
            
            hotels = []
            for place in places_result.get('results', [])[:10]:  # Limit to 10 hotels
                
                # Get additional details
                place_id = place.get('place_id')
                place_details = self.gmaps.place(
                    place_id=place_id,
                    fields=['name', 'rating', 'price_level', 'formatted_address', 'geometry', 'photos', 'reviews']
                )
                
                details = place_details.get('result', {})
                
                hotel = {
                    "name": details.get('name', 'Unknown Hotel'),
                    "rating": details.get('rating', 0),
                    "price_level": details.get('price_level', 2),
                    "address": details.get('formatted_address', ''),
                    "coordinates": details.get('geometry', {}).get('location', {}),
                    "photos": [photo.get('photo_reference', '') for photo in details.get('photos', [])],
                    "reviews": [
                        {
                            "author": review.get('author_name', ''),
                            "rating": review.get('rating', 0),
                            "text": review.get('text', '')[:200] + '...' if len(review.get('text', '')) > 200 else review.get('text', '')
                        }
                        for review in details.get('reviews', [])[:3]
                    ]
                }
                
                # Add estimated price based on price level
                price_ranges = {
                    0: "$50-100",
                    1: "$100-150", 
                    2: "$150-250",
                    3: "$250-400",
                    4: "$400+"
                }
                hotel["estimated_price"] = price_ranges.get(details.get('price_level', 2), "$150-250")
                
                hotels.append(hotel)
            
            # Sort by rating and filter by budget
            hotels = self._filter_by_budget(hotels, budget)
            return sorted(hotels, key=lambda x: x['rating'], reverse=True)
            
        except Exception as e:
            print(f"Error searching hotels: {e}")
            return self._get_mock_hotels(location, budget)

    def _filter_by_budget(self, hotels: List[Dict[str, Any]], budget: str) -> List[Dict[str, Any]]:
        """Filter hotels by budget preference"""
        
        budget_mapping = {
            "cheap": [0, 1],      # $50-150
            "moderate": [1, 2],   # $100-250
            "luxury": [3, 4]      # $250+
        }
        
        allowed_price_levels = budget_mapping.get(budget, [1, 2])
        return [hotel for hotel in hotels if hotel.get('price_level') in allowed_price_levels]

    def _get_mock_hotels(self, location: str, budget: str) -> List[Dict[str, Any]]:
        """Return mock hotel data when API is not available"""
        
        mock_hotels = [
            {
                "name": f"Grand Hotel {location}",
                "rating": 4.5,
                "price_level": 3,
                "address": f"123 Main Street, {location}",
                "coordinates": {"lat": 41.9028, "lng": 12.4964},
                "estimated_price": "$250-400",
                "photos": [],
                "reviews": [
                    {
                        "author": "John Doe",
                        "rating": 5,
                        "text": "Excellent location and service. Highly recommended!"
                    }
                ]
            },
            {
                "name": f"Budget Inn {location}",
                "rating": 3.8,
                "price_level": 1,
                "address": f"456 Oak Avenue, {location}",
                "coordinates": {"lat": 41.9028, "lng": 12.4964},
                "estimated_price": "$100-150",
                "photos": [],
                "reviews": [
                    {
                        "author": "Jane Smith",
                        "rating": 4,
                        "text": "Good value for money. Clean and comfortable."
                    }
                ]
            },
            {
                "name": f"Luxury Resort {location}",
                "rating": 4.8,
                "price_level": 4,
                "address": f"789 Resort Drive, {location}",
                "coordinates": {"lat": 41.9028, "lng": 12.4964},
                "estimated_price": "$400+",
                "photos": [],
                "reviews": [
                    {
                        "author": "Mike Johnson",
                        "rating": 5,
                        "text": "Outstanding luxury experience. Worth every penny!"
                    }
                ]
            }
        ]
        
        # Filter by budget
        filtered_hotels = self._filter_by_budget(mock_hotels, budget)
        return filtered_hotels[:5]  # Return top 5
