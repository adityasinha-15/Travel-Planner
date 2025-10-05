import os
import google.generativeai as genai
from typing import Dict, Any, List
import json

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️  Warning: GEMINI_API_KEY not found, using mock mode")
            self.model = None
            return
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Define tools/functions that Gemini can use
        self.tools = [
            {
                "function_declarations": [
                    {
                        "name": "search_hotels",
                        "description": "Search for hotels in a specific location with given criteria",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "City or location to search hotels in"},
                                "budget": {"type": "string", "description": "Budget preference (cheap, moderate, luxury)"},
                                "nearby": {"type": "string", "description": "Landmark or area to be near to"}
                            },
                            "required": ["location"]
                        }
                    },
                    {
                        "name": "get_weather",
                        "description": "Get weather forecast for a location and date range",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "City or location for weather"},
                                "start_date": {"type": "string", "description": "Start date for weather forecast"},
                                "end_date": {"type": "string", "description": "End date for weather forecast"}
                            },
                            "required": ["location", "start_date", "end_date"]
                        }
                    },
                    {
                        "name": "get_attractions",
                        "description": "Get popular attractions and tourist spots in a location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {"type": "string", "description": "City or location to find attractions in"},
                                "interests": {"type": "string", "description": "Types of attractions (historical, cultural, nature, etc.)"}
                            },
                            "required": ["location"]
                        }
                    },
                    {
                        "name": "get_flights",
                        "description": "Search for flights between locations",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "origin": {"type": "string", "description": "Origin city or airport code"},
                                "destination": {"type": "string", "description": "Destination city or airport code"},
                                "departure_date": {"type": "string", "description": "Departure date"},
                                "return_date": {"type": "string", "description": "Return date (optional)"}
                            },
                            "required": ["origin", "destination", "departure_date"]
                        }
                    },
                    {
                        "name": "get_routes",
                        "description": "Get optimized routes between attractions and hotels",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "start_location": {"type": "string", "description": "Starting location"},
                                "end_location": {"type": "string", "description": "Ending location"},
                                "waypoints": {"type": "array", "items": {"type": "string"}, "description": "Intermediate stops"}
                            },
                            "required": ["start_location", "end_location"]
                        }
                    }
                ]
            }
        ]

    async def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the user prompt and extract trip details"""
        
        if not self.model:
            # Mock analysis when API key is not available
            return self._mock_analyze_prompt(prompt)
        
        system_prompt = """
        You are a smart travel planning assistant. Analyze the user's travel prompt and extract the following information:
        
        1. Destination (city/country)
        2. Duration (number of days)
        3. Travel dates (month/year or specific dates)
        4. Budget preferences (cheap, moderate, luxury)
        5. Specific interests or attractions mentioned
        6. Any special requirements
        
        Respond with a JSON object containing:
        {
            "destination": "extracted destination",
            "duration": number_of_days,
            "dates": "extracted dates or month/year",
            "budget": "cheap/moderate/luxury",
            "interests": ["list", "of", "interests"],
            "requirements": ["any", "special", "requirements"]
        }
        
        If any information is not provided, use reasonable defaults.
        """
        
        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser prompt: {prompt}",
                tools=self.tools
            )
            
            # Extract JSON from response
            response_text = response.text
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                # Try to extract JSON from the response
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                json_str = response_text[start_idx:end_idx]
            
            return json.loads(json_str)
            
        except Exception as e:
            print(f"Error analyzing prompt: {e}")
            return self._mock_analyze_prompt(prompt)

    def _mock_analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Mock prompt analysis when API is not available"""
        prompt_lower = prompt.lower()
        
        # Simple keyword extraction
        destinations = []
        if "rome" in prompt_lower:
            destinations.append("Rome")
        if "paris" in prompt_lower:
            destinations.append("Paris")
        if "london" in prompt_lower:
            destinations.append("London")
        if "tokyo" in prompt_lower:
            destinations.append("Tokyo")
        if "barcelona" in prompt_lower:
            destinations.append("Barcelona")
        if "new york" in prompt_lower:
            destinations.append("New York")
        
        destination = destinations[0] if destinations else "Rome"
        
        # Extract duration
        duration = 3
        if "4-day" in prompt_lower or "4 day" in prompt_lower:
            duration = 4
        elif "5-day" in prompt_lower or "5 day" in prompt_lower:
            duration = 5
        elif "week" in prompt_lower:
            duration = 7
        
        # Extract budget
        budget = "moderate"
        if "budget" in prompt_lower or "cheap" in prompt_lower:
            budget = "cheap"
        elif "luxury" in prompt_lower:
            budget = "luxury"
        
        # Extract dates
        dates = "Not specified"
        if "october" in prompt_lower:
            dates = "October 2024"
        elif "november" in prompt_lower:
            dates = "November 2024"
        elif "spring" in prompt_lower:
            dates = "Spring 2024"
        
        return {
            "destination": destination,
            "duration": duration,
            "dates": dates,
            "budget": budget,
            "interests": ["historical", "cultural"],
            "requirements": []
        }

    async def plan_trip_with_tools(self, prompt: str, tool_results: Dict[str, Any]) -> str:
        """Generate a comprehensive trip plan using tool results"""
        
        if not self.model:
            return self._mock_trip_plan(prompt, tool_results)
        
        plan_prompt = f"""
        Based on the user's request and the data gathered, create a comprehensive travel plan.
        
        User Request: {prompt}
        
        Available Data:
        {json.dumps(tool_results, indent=2)}
        
        Create a detailed travel plan including:
        1. Summary of the trip
        2. Recommended hotels with brief descriptions
        3. Top attractions to visit with suggested itinerary
        4. Weather information and recommendations
        5. Flight options if available
        6. Practical tips and recommendations
        
        Make it engaging and helpful for the traveler.
        """
        
        try:
            response = self.model.generate_content(plan_prompt)
            return response.text
        except Exception as e:
            return self._mock_trip_plan(prompt, tool_results)

    def _mock_trip_plan(self, prompt: str, tool_results: Dict[str, Any]) -> str:
        """Generate mock trip plan when API is not available"""
        destination = tool_results.get("trip_details", {}).get("destination", "Rome")
        duration = tool_results.get("trip_details", {}).get("duration", 3)
        
        return f"""
🎉 Your Amazing {duration}-Day Trip to {destination}!

Welcome to your personalized travel adventure! I've crafted the perfect itinerary for your {duration}-day journey to {destination}. Here's what awaits you:

🏨 **Accommodation**
I've found some fantastic hotels that match your preferences. From cozy budget-friendly options to luxurious resorts, there's something for every traveler.

🗺️ **Must-See Attractions**
{destination} is brimming with incredible sights! I've selected the top attractions that will give you an authentic experience of this beautiful destination.

🌤️ **Weather & Packing Tips**
The weather looks great for your visit! I've included detailed forecasts and packing recommendations to ensure you're comfortable throughout your stay.

✈️ **Getting There**
I've researched the best flight options to get you to {destination} safely and affordably.

💡 **Pro Tips**
- Book attractions in advance to skip the lines
- Try local cuisine - it's part of the adventure!
- Keep copies of important documents
- Download offline maps before you go

This is just the beginning of your amazing journey. Get ready for unforgettable memories in {destination}! 🚀
        """
