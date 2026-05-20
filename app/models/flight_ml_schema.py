from pydantic import BaseModel
from typing import Optional 

class TrainRequest(BaseModel):
    source:str # either "csv" or from "app.state"
    csv_path:Optional[str] = None
    pkl_path:Optional[str] = None