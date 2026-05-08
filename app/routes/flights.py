from fastapi import APIRouter 
from app.services.extractor import FlightExtractor
from app.models.flight_schema import FlightSearchRequest
from app.services.parsers import FlightParser
import time
router = APIRouter(
    prefix='/flights',
    tags=['Flights'])

extractor = FlightExtractor() 
async def raw_flights_fetcher(origin:str,destination:str,depart_date:str,return_date:str|None)->list:
 raw_flights = await extractor.extract(
  origin=origin,
  destination=destination,
  depart_date=depart_date,
  return_date=return_date
 )
 return raw_flights

@router.post('/search') 
async def search_flights(request:FlightSearchRequest):
 if request.timer:
  start_time = time.process_time()
 raw_flights = await raw_flights_fetcher(request.origin,request.destination,request.depart_date,request.return_date)
 parsed_flights = [FlightParser.parse(flight) for flight in raw_flights]
 return {
  "total_flights":len(parsed_flights),
  "flights":parsed_flights,
  "time":(time.process_time() - start_time) if request.timer else None
 }

@router.post('/text_streamer') 
async def get_raw_flights(request:FlightSearchRequest):
 if request.timer:
  start_time=time.process_time() 
 raw_flights = await raw_flights_fetcher(request.origin,request.destination,request.depart_date,request.return_date) 
 return {
  "time":(time.process_time() - start_time) if request.timer else None,
  "data":raw_flights
 }

 