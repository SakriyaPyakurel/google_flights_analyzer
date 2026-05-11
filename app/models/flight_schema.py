from pydantic import BaseModel 
from typing import Optional 

class FlightSearchRequest(BaseModel):
    origin:str
    destination:str 
    depart_date:str 
    return_date:Optional[str] = None
    timer:bool=False

class SaveToCsvRequest(BaseModel):
    override:bool=False 
    pathname:Optional[str] = None

class shufflecsvrequest(BaseModel):
    pathname:Optional[str] = None