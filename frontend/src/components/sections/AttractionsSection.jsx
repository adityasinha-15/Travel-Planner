import React from 'react'
import { MapPin, Star, Clock, DollarSign } from 'lucide-react'

const AttractionsSection = ({ attractions }) => {
  if (!attractions || attractions.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <MapPin className="h-5 w-5 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Attractions</h2>
        </div>
        <p className="text-gray-600">No attractions found for this destination.</p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-3 mb-4">
        <MapPin className="h-5 w-5 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-900">Top Attractions</h2>
      </div>
      
      <div className="space-y-4">
        {attractions.map((attraction, index) => (
          <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-gray-900">{attraction.name}</h3>
              <div className="flex items-center space-x-1">
                <Star className="h-4 w-4 text-yellow-400 fill-current" />
                <span className="text-sm font-medium text-gray-700">
                  {attraction.rating?.toFixed(1) || 'N/A'}
                </span>
              </div>
            </div>
            
            {attraction.category && (
              <div className="mb-2">
                <span className="inline-block bg-primary-100 text-primary-800 text-xs font-medium px-2 py-1 rounded-full">
                  {attraction.category}
                </span>
              </div>
            )}
            
            {attraction.address && (
              <div className="flex items-center space-x-2 text-sm text-gray-600 mb-2">
                <MapPin className="h-4 w-4" />
                <span>{attraction.address}</span>
              </div>
            )}
            
            <div className="flex items-center justify-between text-sm text-gray-600">
              {attraction.estimated_visit_time && (
                <div className="flex items-center space-x-2">
                  <Clock className="h-4 w-4" />
                  <span>{attraction.estimated_visit_time}</span>
                </div>
              )}
              
              {attraction.pricing && (
                <div className="flex items-center space-x-2">
                  <DollarSign className="h-4 w-4" />
                  <span>{attraction.pricing}</span>
                </div>
              )}
            </div>
            
            {attraction.reviews && attraction.reviews.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="text-sm text-gray-600">
                  <p className="font-medium text-gray-700 mb-1">
                    "{attraction.reviews[0].text}"
                  </p>
                  <p className="text-xs text-gray-500">- {attraction.reviews[0].author}</p>
                </div>
              </div>
            )}
            
            {attraction.opening_hours && attraction.opening_hours.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <p className="text-xs font-medium text-gray-700 mb-1">Opening Hours:</p>
                <div className="text-xs text-gray-600 space-y-1">
                  {attraction.opening_hours.slice(0, 3).map((hours, idx) => (
                    <p key={idx}>{hours}</p>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default AttractionsSection
