from fastapi import APIRouter,Request,HTTPException
from app.services.extractor import FlightExtractor
from app.models.flight_schema import FlightSearchRequest,SaveToCsvRequest,shufflecsvrequest
from app.services.parsers import FlightParser
import time
import re
import os
import pandas as pd
router = APIRouter(
    prefix='/flights',
    tags=['Flights'])
extractor = FlightExtractor() 

def duration_to_minutes(duration: str | None) -> int | None:
    if not duration:
        return None

    total_minutes = 0

    hr_match = re.search(r"(\d+)\s*hr", duration)
    min_match = re.search(r"(\d+)\s*min", duration)

    if hr_match:
        total_minutes += int(hr_match.group(1)) * 60

    if min_match:
        total_minutes += int(min_match.group(1))

    return total_minutes

async def raw_flights_fetcher(origin:str,destination:str,depart_date:str,return_date:str|None)->list:
 raw_flights = await extractor.extract(
  origin=origin,
  destination=destination,
  depart_date=depart_date,
  return_date=return_date
 )
 return raw_flights

@router.post('/search') 
async def search_flights(request:FlightSearchRequest,req:Request):
 if request.timer:
  start_time = time.perf_counter()
 raw_flights = await raw_flights_fetcher(request.origin,request.destination,request.depart_date,request.return_date)
 parsed_flights = [FlightParser.parse(flight) for flight in raw_flights]
 simplified_flights = [
        {
            "origin": request.origin,
            "destination": request.destination,
            "departure_date":request.depart_date,
            "return_date":request.return_date,
            "origin_airport": flight.get("departure_airport"),
            "destination_airport": flight.get("arrival_airport"),
            "airline":flight.get("airline"),
            "stops": flight.get("stops"),
            "departure_time": flight.get("departure_time"),
            "arrival_time": flight.get("arrival_time"),
            "duration(in minutes)":  duration_to_minutes(flight.get("duration")),
            "price":flight.get('price'),
            "currency":flight.get('currency')
        }
        for flight in parsed_flights
    ]
 req.app.state.flights_data.extend(simplified_flights)
 return {
  "total_flights":len(parsed_flights),
  "flights":parsed_flights,
  "time":(time.perf_counter - start_time) if request.timer else None
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

@router.post("/save_to_csv")
async def save_flights(request: SaveToCsvRequest, req: Request):

    flights_data = req.app.state.flights_data

    # Ensuring there is data to save
    if not flights_data:
        raise HTTPException(
            status_code=400,
            detail="No flight data available. Run /flights/search first."
        )

    # Determining filename
    if request.pathname:
        filename = os.path.basename(request.pathname)
    else:
        filename = "flights.csv"

    # Ensuring .csv extension present in pathname
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Build full path
    filepath = os.path.join(req.app.state.base_dir, filename)

    # If file exists and override=False, append new data
    # If file exists and override=True, replace file
    # If file does not exist, create it
    if os.path.exists(filepath):
        if request.override:
            mode = "w"   #overwrite
            header = True
        else:
            mode = "a"   # append
            header = False
    else:
        mode = "w"
        header = True

    # Saving to CSV
    df = pd.DataFrame(flights_data)
    df.to_csv(
        filepath,
        mode=mode,
        header=header,
        index=False
    )

    return {
        "status": "success",
        "message": (
            "Flight data overwritten successfully."
            if request.override and os.path.exists(filepath)
            else "Flight data saved successfully."
        ),
        "file_path": filepath,
        "rows_written": len(df),
        "mode": "overwrite" if request.override else ("append" if os.path.exists(filepath) else "create")
    }

@router.post('/shuffle_csv') 
def csv_shuffler(request:shufflecsvrequest,req:Request):
   if request.pathname:
        filename = os.path.basename(request.pathname)
   else:
        filename = "flights.csv"

    # Ensuring .csv extension present in pathname
   if not filename.endswith(".csv"):
        filename += ".csv"

    # Building full path
   filepath = os.path.join(req.app.state.base_dir, filename)
   if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        shuffled_df = df.sample(frac=1).reset_index(drop=True)
        shuffled_df.to_csv(filepath, index=False)
        return {
           "status":"success",
           "message":f"{len(df)} rows shuffled" 
        }
   else:
      raise HTTPException(
            status_code=400,
            detail="The csv file doesnt exist. There's nothing to shuffle."
        )
