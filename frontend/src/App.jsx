import React, { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import TripPlanner from './components/TripPlanner'
import TripResults from './components/TripResults'
import Header from './components/Header'

function App() {
  const [tripData, setTripData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleTripPlan = async (prompt) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/plan-trip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      if (!response.ok) {
        throw new Error('Failed to plan trip')
      }

      const data = await response.json()
      setTripData(data)
    } catch (error) {
      console.error('Error planning trip:', error)
      // You could add toast notifications here
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setTripData(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!tripData ? (
          <TripPlanner onPlanTrip={handleTripPlan} isLoading={isLoading} />
        ) : (
          <TripResults tripData={tripData} onReset={handleReset} />
        )}
      </main>
      
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
    </div>
  )
}

export default App
