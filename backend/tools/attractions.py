import os
import googlemaps
from typing import List, Dict, Any
import json

class AttractionsService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if api_key:
            self.gmaps = googlemaps.Client(key=api_key)
        else:
            self.gmaps = None

    async def get_attractions(self, location: str, interests: List[str] = None) -> List[Dict[str, Any]]:
        """Get popular attractions and tourist spots in a location"""
        
        if not self.gmaps:
            return self._get_mock_attractions(location, interests)
        
        try:
            attractions = []
            
            # Define search types based on interests
            search_types = self._get_search_types(interests)
            
            for search_type in search_types:
                # Search for places
                places_result = self.gmaps.places_nearby(
                    location=location,
                    radius=10000,  # 10km radius
                    type=search_type
                )
                
                for place in places_result.get('results', [])[:5]:  # Limit per type
                    
                    # Get additional details
                    place_id = place.get('place_id')
                    place_details = self.gmaps.place(
                        place_id=place_id,
                        fields=['name', 'rating', 'price_level', 'formatted_address', 
                               'geometry', 'photos', 'reviews', 'opening_hours', 'types']
                    )
                    
                    details = place_details.get('result', {})
                    
                    attraction = {
                        "name": details.get('name', 'Unknown Attraction'),
                        "rating": details.get('rating', 0),
                        "price_level": details.get('price_level', 0),
                        "address": details.get('formatted_address', ''),
                        "coordinates": details.get('geometry', {}).get('location', {}),
                        "photos": [photo.get('photo_reference', '') for photo in details.get('photos', [])],
                        "types": details.get('types', []),
                        "opening_hours": details.get('opening_hours', {}).get('weekday_text', []),
                        "reviews": [
                            {
                                "author": review.get('author_name', ''),
                                "rating": review.get('rating', 0),
                                "text": review.get('text', '')[:200] + '...' if len(review.get('text', '')) > 200 else review.get('text', '')
                            }
                            for review in details.get('reviews', [])[:3]
                        ]
                    }
                    
                    # Add category and estimated visit time
                    attraction["category"] = self._get_category(search_type)
                    attraction["estimated_visit_time"] = self._estimate_visit_time(search_type)
                    
                    # Add pricing info
                    if details.get('price_level') == 0:
                        attraction["pricing"] = "Free"
                    elif details.get('price_level') == 1:
                        attraction["pricing"] = "$5-15"
                    elif details.get('price_level') == 2:
                        attraction["pricing"] = "$15-30"
                    elif details.get('price_level') == 3:
                        attraction["pricing"] = "$30-50"
                    else:
                        attraction["pricing"] = "$50+"
                    
                    attractions.append(attraction)
            
            # Remove duplicates and sort by rating
            unique_attractions = self._remove_duplicates(attractions)
            return sorted(unique_attractions, key=lambda x: x['rating'], reverse=True)[:15]
            
        except Exception as e:
            print(f"Error fetching attractions: {e}")
            return self._get_mock_attractions(location, interests)

    def _get_search_types(self, interests: List[str] = None) -> List[str]:
        """Get Google Places API types based on user interests"""
        
        if not interests:
            return ['tourist_attraction', 'museum', 'park', 'shopping_mall', 'restaurant']
        
        type_mapping = {
            'historical': ['tourist_attraction', 'museum', 'church'],
            'cultural': ['museum', 'art_gallery', 'theater'],
            'nature': ['park', 'zoo', 'aquarium'],
            'shopping': ['shopping_mall', 'store'],
            'food': ['restaurant', 'food'],
            'entertainment': ['amusement_park', 'movie_theater', 'night_club'],
            'sports': ['stadium', 'gym', 'sports_complex']
        }
        
        search_types = set()
        for interest in interests:
            if interest.lower() in type_mapping:
                search_types.update(type_mapping[interest.lower()])
        
        # If no specific interests match, return default types
        if not search_types:
            search_types = {'tourist_attraction', 'museum', 'park'}
        
        return list(search_types)

    def _get_category(self, search_type: str) -> str:
        """Get human-readable category from Google Places type"""
        
        category_mapping = {
            'tourist_attraction': 'Tourist Attraction',
            'museum': 'Museum',
            'church': 'Religious Site',
            'art_gallery': 'Art Gallery',
            'theater': 'Theater',
            'park': 'Park',
            'zoo': 'Zoo',
            'aquarium': 'Aquarium',
            'shopping_mall': 'Shopping',
            'restaurant': 'Restaurant',
            'amusement_park': 'Entertainment',
            'movie_theater': 'Entertainment',
            'night_club': 'Nightlife',
            'stadium': 'Sports'
        }
        
        return category_mapping.get(search_type, 'Attraction')

    def _estimate_visit_time(self, search_type: str) -> str:
        """Estimate how long visitors typically spend at an attraction"""
        
        time_mapping = {
            'tourist_attraction': '2-4 hours',
            'museum': '2-3 hours',
            'church': '30 minutes - 1 hour',
            'art_gallery': '1-2 hours',
            'theater': '2-3 hours',
            'park': '1-3 hours',
            'zoo': '3-5 hours',
            'aquarium': '2-3 hours',
            'shopping_mall': '1-4 hours',
            'restaurant': '1-2 hours',
            'amusement_park': '4-8 hours',
            'movie_theater': '2-3 hours',
            'night_club': '3-5 hours',
            'stadium': '2-4 hours'
        }
        
        return time_mapping.get(search_type, '1-2 hours')

    def _remove_duplicates(self, attractions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate attractions based on name"""
        
        seen = set()
        unique_attractions = []
        
        for attraction in attractions:
            name = attraction['name'].lower()
            if name not in seen:
                seen.add(name)
                unique_attractions.append(attraction)
        
        return unique_attractions

    def _get_mock_attractions(self, location: str, interests: List[str] = None) -> List[Dict[str, Any]]:
        """Return mock attraction data when API is not available"""
        
        mock_attractions = [
            {
                "name": f"Historic Center of {location}",
                "rating": 4.7,
                "price_level": 0,
                "pricing": "Free",
                "address": f"City Center, {location}",
                "coordinates": {"lat": 41.9028, "lng": 12.4964},
                "category": "Tourist Attraction",
                "estimated_visit_time": "3-4 hours",
                "photos": [],
                "types": ["tourist_attraction"],
                "opening_hours": ["Open 24 hours"],
                "reviews": [
                    {
                        "author": "Sarah Wilson",
                        "rating": 5,
                        "text": "Absolutely beautiful historic area. Must visit!"
                    }
                ]
            },
            {
                "name": f"{location} National Museum",
                "rating": 4.5,
                "price_level": 2,
                "pricing": "$15-30",
                "address": f"Museum District, {location}",
                "coordinates": {"lat": 41.9028, "lng": 12.4964},
                "category": "Museum",
                "estimated_visit_time": "2-3 hours",
                "photos": [],
                "types": ["museum"],
                "opening_hours": ["Tuesday-Sunday: 9:00 AM - 5:00 PM"],
                "reviews": [
                    {
                        "author": "David Brown",
                        "rating": 4,
                        "text": "Great collection of local history and art."
                    }
                ]
            },
            {
                "name": f"{location} Central Park",
                "rating": 4.3,
                "price_level": 0,
                "pricing": "Free",
                "address": f"Central District, {location}",
                "coordinates": {"lat": 41.9028, "lng": 12.4964},
                "category": "Park",
                "estimated_visit_time": "1-3 hours",
                "photos": [],
                "types": ["park"],
                "opening_hours": ["Open 24 hours"],
                "reviews": [
                    {
                        "author": "Lisa Garcia",
                        "rating": 4,
                        "text": "Perfect place for a relaxing walk and picnic."
                    }
                ]
            }
        ]
        
        return mock_attractions
