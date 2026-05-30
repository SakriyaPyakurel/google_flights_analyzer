import pandas as pd

def prepare_features(df: pd.DataFrame):
    df = df.copy()

    df["departure_date"] = pd.to_datetime(df["departure_date"])
    df["return_date"] = pd.to_datetime(df["return_date"])

    df["trip_length"] = (
        df["return_date"] - df["departure_date"]
    ).dt.days
    
    # Departure features
    df["departure_day"] = df["departure_date"].dt.day
    df["departure_month"] = df["departure_date"].dt.month
    df["departure_dayofweek"] = df["departure_date"].dt.dayofweek
    df["departure_week"] = df["departure_date"].dt.isocalendar().week.astype(int)
    # Return features
    df["return_day"] = df["return_date"].dt.day
    df["return_month"] = df["return_date"].dt.month
    df["return_dayofweek"] = df["return_date"].dt.dayofweek
    # Times feature
    df["departure_hour"] = pd.to_datetime(
        df["departure_time"]
    ).dt.hour
    df["arrival_hour"] = pd.to_datetime(
        df["arrival_time"]
    ).dt.hour
    # Indicator of weekend
    df["is_weekend_departure"] = (
        df["departure_dayofweek"] >= 5
    ).astype(int)
     # Airline stop interaction feature
    df["airline_stop"] = (
    df["airline"] + "_" +
    df["stops"].astype(str)
)
    
    df["scraped_at"] = pd.to_datetime(df["scrape_time"])
    df["days_until_departure"] = (
    df["departure_date"] - df["scraped_at"]
).dt.days
    df.drop_duplicates(inplace=True)
    return df