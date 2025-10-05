from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn

from tools.gemini_client import GeminiClient
from tools.trip_planner import TripPlanner

# Load environment variables
load_dotenv()

app = FastAPI(title="Smart Travel Planner API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_client = GeminiClient()
trip_planner = TripPlanner()

class TripRequest(BaseModel):
    prompt: str

class TripResponse(BaseModel):
    destination: str
    duration: int
    dates: str
    hotels: list
    attractions: list
    weather: dict
    flights: list
    routes: list
    summary: str

@app.get("/")
async def root():
    return {"message": "Smart Travel Planner API is running!"}

@app.post("/plan-trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    try:
        # Use Gemini to analyze the prompt and plan the trip
        trip_plan = await trip_planner.plan_trip(request.prompt)
        return TripResponse(**trip_plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
