from fastapi import APIRouter 
from app.services.extractor import FlightExtractor
from app.models.flight_schema import FlightSearchRequest
from app.services.parsers import FlightParser
router = APIRouter(
    prefix='/flights',
    tags=['Flights'])

@router.post('/search') 
async def search_flights(request:FlightSearchRequest):
 extractor = FlightExtractor() 
 raw_flights = await extractor.extract(
  origin=request.origin,
  destination=request.destination,
  depart_date=request.depart_date,
  return_date=request.return_date
 )
 
 parsed_flights = [FlightParser.parse(flight) for flight in raw_flights]
 return {
  "total_flights":len(parsed_flights),
  "flights":parsed_flights
 }