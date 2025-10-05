import React from 'react'
import { Plane, Clock, DollarSign, MapPin } from 'lucide-react'

const FlightsSection = ({ flights }) => {
  if (!flights || flights.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Plane className="h-5 w-5 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Flights</h2>
        </div>
        <p className="text-gray-600">Flight information not available.</p>
      </div>
    )
  }

  const formatDuration = (durationStr) => {
    if (!durationStr) return 'N/A'
    
    // Handle PT format (e.g., "PT2H30M")
    if (durationStr.startsWith('PT')) {
      const match = durationStr.match(/PT(?:(\d+)H)?(?:(\d+)M)?/)
      if (match) {
        const hours = match[1] ? `${match[1]}h` : ''
        const minutes = match[2] ? `${match[2]}m` : ''
        return `${hours}${minutes}`.trim() || 'N/A'
      }
    }
    
    // Handle other formats
    return durationStr
  }

  const formatTime = (timeStr) => {
    if (!timeStr) return 'N/A'
    
    try {
      const date = new Date(timeStr)
      return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      })
    } catch {
      return timeStr
    }
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-3 mb-4">
        <Plane className="h-5 w-5 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-900">Flight Options</h2>
      </div>
      
      <div className="space-y-4">
        {flights.map((flight, index) => (
          <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            {/* Flight Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="bg-primary-100 p-2 rounded-full">
                  <Plane className="h-4 w-4 text-primary-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">
                    {flight.airline || 'Flight'}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {flight.stops === 0 ? 'Direct' : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}
                  </p>
                </div>
              </div>
              
              <div className="text-right">
                <p className="text-xl font-bold text-gray-900">
                  {flight.price?.currency} {flight.price?.total}
                </p>
                <p className="text-sm text-gray-600">
                  {flight.duration_hours ? `${flight.duration_hours}h total` : 'Duration varies'}
                </p>
              </div>
            </div>
            
            {/* Flight Details */}
            {flight.itineraries && flight.itineraries.length > 0 && (
              <div className="space-y-3">
                {flight.itineraries.map((itinerary, itinIndex) => (
                  <div key={itinIndex}>
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                      <span>Duration: {formatDuration(itinerary.duration)}</span>
                    </div>
                    
                    {itinerary.segments && itinerary.segments.length > 0 && (
                      <div className="space-y-2">
                        {itinerary.segments.map((segment, segIndex) => (
                          <div key={segIndex} className="flex items-center justify-between bg-white p-3 rounded border">
                            <div className="flex items-center space-x-4">
                              <div className="text-center">
                                <p className="font-semibold text-gray-900">
                                  {formatTime(segment.departure?.time)}
                                </p>
                                <p className="text-xs text-gray-600">
                                  {segment.departure?.airport}
                                </p>
                                {segment.departure?.terminal && (
                                  <p className="text-xs text-gray-500">
                                    Terminal {segment.departure.terminal}
                                  </p>
                                )}
                              </div>
                              
                              <div className="flex items-center space-x-2">
                                <div className="w-8 h-px bg-gray-300"></div>
                                <Plane className="h-3 w-3 text-gray-400" />
                                <div className="w-8 h-px bg-gray-300"></div>
                              </div>
                              
                              <div className="text-center">
                                <p className="font-semibold text-gray-900">
                                  {formatTime(segment.arrival?.time)}
                                </p>
                                <p className="text-xs text-gray-600">
                                  {segment.arrival?.airport}
                                </p>
                                {segment.arrival?.terminal && (
                                  <p className="text-xs text-gray-500">
                                    Terminal {segment.arrival.terminal}
                                  </p>
                                )}
                              </div>
                            </div>
                            
                            <div className="text-right">
                              <p className="text-sm font-medium text-gray-900">
                                {segment.carrier_code} {segment.flight_number}
                              </p>
                              {segment.aircraft && (
                                <p className="text-xs text-gray-600">
                                  {segment.aircraft}
                                </p>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> Flight prices and availability are subject to change. 
          Please check with airlines directly for the most current information and to book.
        </p>
      </div>
    </div>
  )
}

export default FlightsSection
