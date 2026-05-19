import joblib 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,r2_score 

class FlightPriceTrainer:
    def __init__(self):
        self.model = None 
    def train(self,df):
        target = "price" 
        features = [
            "origin",
            "destination",
            "airline",
            "stops",
            "duration(in minutes)",
            "trip_length",
            "departure_hour",
            "arrival_hour",
            "departure_dayofweek",
            "departure_month",
        ]

        X = df[features]
        y = df[target]

        X_train, X_test, Y_train, Y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42
        )

        categorical = [
            "origin",
            "destination",
            "airline"
        ]

        numeric = [
            "stops",
            "duration(in minutes)",
            "trip_length",
            "departure_hour",
            "arrival_hour",
            "departure_dayofweek",
            "departure_month",
        ]

        preprocessor = ColumnTransformer([
            ("cat",
             OneHotEncoder(handle_unknown='ignore'),
             categorical
             ),
             ("num",
              "passthrough",
              numeric
              )
        ])

        self.model = Pipeline([
            ("preprocessor",preprocessor),
            ("regressor",RandomForestRegressor(
                n_estimators=200,
                random_state=42
            ))
        ])
        self.model.fit(X_train,Y_train)
        preds = self.model.predict(X_test) 

        return {
            "mae":mean_absolute_error(Y_test,preds),
            "r2":r2_score(Y_test,preds) 
        }
    
    def save(self,path="flight_models/flight_price_model.pkl"):
       joblib.dump(self.model,path)


