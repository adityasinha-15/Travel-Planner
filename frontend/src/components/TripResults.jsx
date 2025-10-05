import React from 'react'
import { ArrowLeft, MapPin, Calendar, Clock, DollarSign } from 'lucide-react'
import HotelsSection from './sections/HotelsSection'
import AttractionsSection from './sections/AttractionsSection'
import WeatherSection from './sections/WeatherSection'
import FlightsSection from './sections/FlightsSection'
import SummarySection from './sections/SummarySection'

const TripResults = ({ tripData, onReset }) => {
  return (
    <div className="max-w-7xl mx-auto">
      {/* Header with trip overview */}
      <div className="card mb-8">
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={onReset}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Plan Another Trip</span>
          </button>
        </div>

        <div className="flex items-center space-x-6 mb-6">
          <div className="flex items-center space-x-2">
            <MapPin className="h-5 w-5 text-primary-600" />
            <span className="text-lg font-semibold text-gray-900">{tripData.destination}</span>
          </div>
          <div className="flex items-center space-x-2 text-gray-600">
            <Calendar className="h-4 w-4" />
            <span>{tripData.dates}</span>
          </div>
          <div className="flex items-center space-x-2 text-gray-600">
            <Clock className="h-4 w-4" />
            <span>{tripData.duration} days</span>
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Your Trip to {tripData.destination}
        </h1>
        <p className="text-gray-600">
          Here's your personalized travel plan with hotels, attractions, weather, and more!
        </p>
      </div>

      {/* Trip Summary */}
      <SummarySection summary={tripData.summary} />

      {/* Weather Section */}
      <WeatherSection weather={tripData.weather} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Hotels Section */}
        <HotelsSection hotels={tripData.hotels} />

        {/* Attractions Section */}
        <AttractionsSection attractions={tripData.attractions} />
      </div>

      {/* Flights Section */}
      <FlightsSection flights={tripData.flights} />

      {/* Routes Section (if available) */}
      {tripData.routes && tripData.routes.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Suggested Routes</h2>
          <div className="space-y-4">
            {tripData.routes.map((route, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900">
                      {route.start_attraction} → {route.end_attraction}
                    </p>
                    <p className="text-sm text-gray-600">
                      Distance: {route.total_distance} • Duration: {route.total_duration}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default TripResults
