from fastapi import APIRouter, Request, HTTPException
import pandas as pd
from app.models.flight_ml_schema import TrainRequest
from app.services.feature_engineering import prepare_features
from app.services.model_trainer import FlightPriceTrainer
import os

router = APIRouter(prefix="/ml", tags=["Machine Learning in flights data"])

@router.post("/train")
def train_model(request_data: TrainRequest, request: Request):
    if request_data.source == "state":
        data = request.app.state.flights_data
        if not data:
            raise HTTPException(
                status_code=400,
                detail="No flight data in app state."
            )
        df = pd.DataFrame(data)

    elif request_data.source == "csv":
        if not request_data.csv_path:
            raise HTTPException(
                status_code=400,
                detail="csv_path is required."
            )
        filename = request_data.csv_path 
        if not filename.endswith(".csv"):
            filename+=".csv" 
        filepath = os.path.join(request.app.state.base_dir,filename)
        if not os.path.exists(filepath):
              raise HTTPException(status_code=404,
                                 detail="CSV file not found."
    )
        df = pd.read_csv(filepath)

    else:
        raise HTTPException(
            status_code=400,
            detail="source must be 'state' or 'csv'."
        )

    df = prepare_features(df)

    trainer = FlightPriceTrainer()
    metrics = trainer.train(df,tuner=True) if request_data.tune else trainer.train(df)
    if request_data.source == "csv":
        if not request_data.pkl_path:
           trainer.save()
        else:
            filename = request_data.pkl_path
            if not filename.endswith(".pkl"):
                filename+=".pkl" 
            filepath = os.path.join(request.app.state.ml_dir, filename)
            trainer.save(filepath)   
    else:
        request.app.state.flight_quick_model = trainer.model
    return {
        "message": f"Model trained successfully through {request_data.source}.",
        "metrics": metrics,
        "model_path":filepath if request_data.pkl_path else None  
    }