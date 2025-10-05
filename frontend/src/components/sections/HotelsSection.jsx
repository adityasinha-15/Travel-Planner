import React from 'react'
import { Hotel, Star, MapPin, DollarSign } from 'lucide-react'

const HotelsSection = ({ hotels }) => {
  if (!hotels || hotels.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Hotel className="h-5 w-5 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Hotels</h2>
        </div>
        <p className="text-gray-600">No hotels found for this destination.</p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-3 mb-4">
        <Hotel className="h-5 w-5 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-900">Recommended Hotels</h2>
      </div>
      
      <div className="space-y-4">
        {hotels.map((hotel, index) => (
          <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-gray-900">{hotel.name}</h3>
              <div className="flex items-center space-x-1">
                <Star className="h-4 w-4 text-yellow-400 fill-current" />
                <span className="text-sm font-medium text-gray-700">
                  {hotel.rating?.toFixed(1) || 'N/A'}
                </span>
              </div>
            </div>
            
            {hotel.address && (
              <div className="flex items-center space-x-2 text-sm text-gray-600 mb-2">
                <MapPin className="h-4 w-4" />
                <span>{hotel.address}</span>
              </div>
            )}
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <DollarSign className="h-4 w-4" />
                <span>{hotel.estimated_price || hotel.pricing || 'Price not available'}</span>
              </div>
              
              {hotel.price_level !== undefined && (
                <div className="flex space-x-1">
                  {[...Array(4)].map((_, i) => (
                    <DollarSign
                      key={i}
                      className={`h-3 w-3 ${
                        i < hotel.price_level ? 'text-green-600' : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
              )}
            </div>
            
            {hotel.reviews && hotel.reviews.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="text-sm text-gray-600">
                  <p className="font-medium text-gray-700 mb-1">
                    "{hotel.reviews[0].text}"
                  </p>
                  <p className="text-xs text-gray-500">- {hotel.reviews[0].author}</p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default HotelsSection
