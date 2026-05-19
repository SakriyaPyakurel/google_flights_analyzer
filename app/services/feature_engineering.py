import pandas as pd

def prepare_features(df: pd.DataFrame):
    df = df.copy()

    df["departure_date"] = pd.to_datetime(df["departure_date"])
    df["return_date"] = pd.to_datetime(df["return_date"])

    df["trip_length"] = (
        df["return_date"] - df["departure_date"]
    ).dt.days

    df["departure_hour"] = pd.to_datetime(
        df["departure_time"]
    ).dt.hour

    df["arrival_hour"] = pd.to_datetime(
        df["arrival_time"]
    ).dt.hour

    df["departure_dayofweek"] = df["departure_date"].dt.dayofweek
    df["departure_month"] = df["departure_date"].dt.month

    return df