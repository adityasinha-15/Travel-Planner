import React, { useState } from 'react'
import { Send, Sparkles, MapPin, Calendar, DollarSign } from 'lucide-react'

const TripPlanner = ({ onPlanTrip, isLoading }) => {
  const [prompt, setPrompt] = useState('')

  const examplePrompts = [
    "Plan a 4-day trip to Rome in October with budget hotels near Colosseum",
    "Plan a 5-day trip to Paris in November with cheap hotels near Eiffel Tower",
    "Plan a 3-day weekend getaway to Barcelona with luxury hotels",
    "Plan a week-long trip to Tokyo in spring with moderate budget"
  ]

  const handleSubmit = (e) => {
    e.preventDefault()
    if (prompt.trim()) {
      onPlanTrip(prompt.trim())
    }
  }

  const handleExampleClick = (examplePrompt) => {
    setPrompt(examplePrompt)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="bg-primary-100 p-3 rounded-full">
            <Sparkles className="h-8 w-8 text-primary-600" />
          </div>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Plan Your Perfect Trip
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Just tell us what you want and our AI will create a complete travel plan with 
          hotels, attractions, weather, and more!
        </p>
      </div>

      <div className="card max-w-3xl mx-auto">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="trip-prompt" className="block text-sm font-medium text-gray-700 mb-2">
              Describe your dream trip
            </label>
            <textarea
              id="trip-prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Example: Plan a 4-day trip to Rome in October with budget hotels near Colosseum, list attractions, weather forecast, and cheapest flights."
              className="input-field min-h-[120px] resize-none"
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            disabled={!prompt.trim() || isLoading}
            className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Planning your trip...</span>
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                <span>Plan My Trip</span>
              </>
            )}
          </button>
        </form>
      </div>

      <div className="mt-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
          Need inspiration? Try these examples:
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-3xl mx-auto">
          {examplePrompts.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              disabled={isLoading}
              className="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  {index === 0 && <MapPin className="h-4 w-4 text-primary-600 mt-1" />}
                  {index === 1 && <Calendar className="h-4 w-4 text-primary-600 mt-1" />}
                  {index === 2 && <DollarSign className="h-4 w-4 text-primary-600 mt-1" />}
                  {index === 3 && <Sparkles className="h-4 w-4 text-primary-600 mt-1" />}
                </div>
                <p className="text-sm text-gray-700">{example}</p>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default TripPlanner
