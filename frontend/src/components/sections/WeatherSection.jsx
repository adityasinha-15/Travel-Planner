import React from 'react'
import { Cloud, Sun, CloudRain, Thermometer, Droplets, Wind } from 'lucide-react'

const WeatherSection = ({ weather }) => {
  if (!weather) {
    return (
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Cloud className="h-5 w-5 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Weather</h2>
        </div>
        <p className="text-gray-600">Weather information not available.</p>
      </div>
    )
  }

  const getWeatherIcon = (description) => {
    const desc = description.toLowerCase()
    if (desc.includes('sun') || desc.includes('clear')) {
      return <Sun className="h-6 w-6 text-yellow-500" />
    } else if (desc.includes('rain') || desc.includes('storm')) {
      return <CloudRain className="h-6 w-6 text-blue-500" />
    } else {
      return <Cloud className="h-6 w-6 text-gray-500" />
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    })
  }

  return (
    <div className="card mb-8">
      <div className="flex items-center space-x-3 mb-4">
        <Cloud className="h-5 w-5 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-900">Weather Forecast</h2>
      </div>
      
      {/* Current Weather */}
      {weather.current && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Current Weather</h3>
              <p className="text-gray-600">{weather.location}</p>
            </div>
            {getWeatherIcon(weather.current.description)}
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex items-center space-x-2">
              <Thermometer className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-2xl font-bold text-gray-900">
                  {weather.current.temperature}°C
                </p>
                <p className="text-sm text-gray-600">
                  Feels like {weather.current.feels_like}°C
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Droplets className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-lg font-semibold text-gray-900">
                  {weather.current.humidity}%
                </p>
                <p className="text-sm text-gray-600">Humidity</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Wind className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-lg font-semibold text-gray-900">
                  {weather.current.wind_speed} m/s
                </p>
                <p className="text-sm text-gray-600">Wind Speed</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Cloud className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-lg font-semibold text-gray-900 capitalize">
                  {weather.current.description}
                </p>
                <p className="text-sm text-gray-600">Condition</p>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Forecast */}
      {weather.forecast && weather.forecast.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">5-Day Forecast</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {weather.forecast.map((day, index) => (
              <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium text-gray-900">
                    {formatDate(day.date)}
                  </h4>
                  {getWeatherIcon(day.description)}
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">High</span>
                    <span className="font-semibold text-gray-900">{day.max_temp}°C</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Low</span>
                    <span className="font-semibold text-gray-900">{day.min_temp}°C</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Humidity</span>
                    <span className="text-sm text-gray-900">{day.humidity}%</span>
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mt-3 capitalize">
                  {day.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Recommendations */}
      {weather.recommendations && weather.recommendations.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Weather Tips</h3>
          <div className="space-y-2">
            {weather.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-primary-600 rounded-full mt-2 flex-shrink-0"></div>
                <p className="text-sm text-gray-700">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default WeatherSection
