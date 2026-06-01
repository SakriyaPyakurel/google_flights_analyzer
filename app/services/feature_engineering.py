import pandas as pd

def get_period(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

def prepare_features(df: pd.DataFrame):
    df = df.copy()

    df["departure_date"] = pd.to_datetime(df["departure_date"])
    df["has_return"] = df["return_date"].notna().astype(int)
    df["return_date"] = pd.to_datetime(df["return_date"],errors="coerce")
    df["trip_length"] = (
    df["return_date"] - df["departure_date"]
).dt.days
    df["trip_length"] = df['trip_length'].fillna(0)
    # Departure features
    df["departure_day"] = df["departure_date"].dt.day
    df["departure_month"] = df["departure_date"].dt.month
    df["departure_dayofweek"] = df["departure_date"].dt.dayofweek
    df["departure_week"] = df["departure_date"].dt.isocalendar().week.astype(int)
    # Return features
    df["return_day"] = df["return_date"].dt.day.fillna(0)
    df["return_month"] = df["return_date"].dt.month.fillna(0)
    df["return_dayofweek"] = df["return_date"].dt.dayofweek.fillna(0)
    # Times feature
    df["departure_hour"] = pd.to_datetime(
        df["departure_time"]
    ).dt.hour
    df["departure_period"] = (
    df["departure_hour"]
    .apply(get_period)
)
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
    df["route"] = (df["origin"] + "_" + df["destination"]) 
    df["route_airline"] = (df["route"] + "_" + df["airline"])
    df["scraped_at"] = pd.to_datetime(df["scrape_time"])
    df["days_until_departure"] = (
    df["departure_date"] - df["scraped_at"]
).dt.days
    # stop duration feature
    df["duration_per_stop"] = (
    df["duration(in minutes)"] /
    (df["stops"] + 1)
)
    df.drop_duplicates(inplace=True)
    return df