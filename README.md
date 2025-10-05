# Smart Travel Planner

An AI-powered travel planning web application that uses Google Gemini to understand natural language prompts and create comprehensive travel itineraries with hotels, attractions, weather forecasts, and flight information.

## Features

- **Natural Language Processing**: Describe your trip in plain English
- **AI-Powered Planning**: Uses Google Gemini API for intelligent trip analysis
- **Comprehensive Data**: Integrates multiple APIs for complete travel information
- **Modern UI**: Beautiful React frontend with Tailwind CSS
- **Real-time Data**: Live weather, hotel, and flight information

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Google Gemini API**: AI/ML for natural language processing
- **Google Maps API**: Places, Directions, and Geocoding
- **OpenWeather API**: Weather forecasts
- **Amadeus API**: Flight search (optional)

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Google Maps JavaScript API**: Interactive maps

## Project Structure

```
Travel Planner/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── requirements.txt        # Python dependencies
│   ├── env.example            # Environment variables template
│   └── tools/
│       ├── __init__.py
│       ├── gemini_client.py   # Gemini API integration
│       ├── trip_planner.py    # Main trip planning logic
│       ├── hotels.py          # Hotels API service
│       ├── weather.py         # Weather API service
│       ├── attractions.py     # Attractions API service
│       ├── flights.py         # Flights API service
│       └── routes.py          # Routes API service
├── frontend/
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind configuration
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── components/
│           ├── Header.jsx
│           ├── TripPlanner.jsx
│           ├── TripResults.jsx
│           └── sections/
│               ├── SummarySection.jsx
│               ├── HotelsSection.jsx
│               ├── AttractionsSection.jsx
│               ├── WeatherSection.jsx
│               └── FlightsSection.jsx
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- API keys for:
  - Google Gemini API
  - Google Maps API
  - OpenWeather API
  - Amadeus API (optional)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   cp env.example .env
   ```

5. Edit `.env` file with your API keys:
   ```env
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   AMADEUS_API_KEY=your_amadeus_api_key_here
   AMADEUS_API_SECRET=your_amadeus_api_secret_here
   HOST=localhost
   PORT=8000
   ```

6. Run the backend server:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## API Key Setup

### Google Gemini API

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### Google Maps API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Places API
   - Directions API
   - Geocoding API
   - Maps JavaScript API
3. Create credentials (API Key)
4. Add it to your `.env` file as `GOOGLE_MAPS_API_KEY`

### OpenWeather API

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key
4. Add it to your `.env` file as `OPENWEATHER_API_KEY`

### Amadeus API (Optional)

1. Go to [Amadeus for Developers](https://developers.amadeus.com/)
2. Sign up for a free account
3. Create a new app to get API key and secret
4. Add them to your `.env` file as `AMADEUS_API_KEY` and `AMADEUS_API_SECRET`

## Usage

1. Start both the backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Enter a natural language prompt like:
   - "Plan a 4-day trip to Rome in October with budget hotels near Colosseum"
   - "Plan a 5-day trip to Paris in November with cheap hotels near Eiffel Tower"
   - "Plan a week-long trip to Tokyo in spring with luxury accommodations"

4. The AI will analyze your request and provide:
   - Hotel recommendations with ratings and prices
   - Popular attractions with visiting times
   - Weather forecast for your travel dates
   - Flight options (if available)
   - Optimized routes between locations

## Features in Detail

### AI-Powered Trip Analysis

The system uses Google Gemini to:
- Extract destination, dates, and preferences from natural language
- Determine budget levels and interests
- Generate comprehensive trip summaries

### Hotel Search

- Uses Google Places API to find hotels
- Filters by budget and location preferences
- Provides ratings, prices, and reviews

### Attractions Discovery

- Searches for tourist attractions based on interests
- Categorizes by type (historical, cultural, nature, etc.)
- Estimates visit times and provides pricing information

### Weather Integration

- Real-time weather forecasts
- 5-day weather predictions
- Travel recommendations based on weather conditions

### Flight Search

- Integration with Amadeus API for flight options
- Displays prices, durations, and stops
- Shows detailed flight itineraries

## Development

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm run build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **API Key Errors**: Make sure all API keys are correctly set in the `.env` file
2. **CORS Issues**: Ensure the frontend is running on the correct port (3000)
3. **Module Not Found**: Make sure you've installed all dependencies
4. **Rate Limiting**: Some APIs have rate limits; the app includes mock data as fallbacks

### Getting Help

- Check the console for error messages
- Verify API keys are active and have proper permissions
- Ensure all required APIs are enabled in Google Cloud Console

## Future Enhancements

- [ ] User authentication and saved trips
- [ ] Interactive maps with custom markers
- [ ] Booking integration with hotels and flights
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Advanced filtering and sorting options
- [ ] Trip sharing and collaboration features
