from fastapi import APIRouter, Request, HTTPException
import pandas as pd
from app.models.flight_ml_schema import TrainRequest
from app.services.feature_engineering import prepare_features
from app.services.model_trainer import FlightPriceTrainer

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

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
        df = pd.read_csv(request_data.csv_path)

    else:
        raise HTTPException(
            status_code=400,
            detail="source must be 'state' or 'csv'."
        )

    df = prepare_features(df)

    trainer = FlightPriceTrainer()
    metrics = trainer.train(df)
    trainer.save()

    return {
        "message": "Model trained successfully.",
        "metrics": metrics
    }