from pydantic import BaseModel 
from typing import Optional 

class FlightSearchRequest(BaseModel):
    origin:str
    destination:str 
    depart_date:str 
    return_date:Optional[str] = None
    timer:bool=False