import joblib 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import mean_absolute_error,r2_score 

class FlightPriceTrainer:
    def __init__(self):
        self.model = None 
    def train(self,df,tuner:bool=False):
        target = "price" 
        features = [
            "origin",
            "destination",
            "airline",
            "origin_airport",
            "destination_airport",
            "route",
            "trip_length",
            "departure_hour",
            "arrival_hour",
            "departure_day",
            "departure_month",
            "departure_dayofweek",
            "departure_week",
            "return_day",
            "return_month",
            "return_dayofweek",
            "stops",
            "duration(in minutes)"
        ]

        X = df[features]
        y = df[target]
        X_train, X_test, Y_train, Y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42
        )

        categorical = [
            "airline",
            "origin",
            "destination",
            "origin_airport",
            "destination_airport",
            "route"
        ]

        numeric = [
            "trip_length",
            "departure_hour",
            "arrival_hour",
            "departure_day",
            "departure_month",
            "departure_dayofweek",
            "departure_week",
            "return_day",
            "return_month",
            "return_dayofweek",
            "stops",
            "duration(in minutes)"
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

        pipeline = Pipeline([
            ("preprocessor",preprocessor),
            ("regressor",RandomForestRegressor(
                random_state=42
            ))
        ])
        # Normal training
        if not tuner:
           pipeline.set_params(
            regressor__n_estimators=200
        )
           self.model = pipeline
           self.model.fit(X_train, Y_train)
        # Hyperparameter tuning
        else:
            param_grid = {
            "regressor__n_estimators": [100, 200],
            "regressor__max_depth": [None, 10, 20],
            "regressor__min_samples_split": [2, 5],
            "regressor__min_samples_leaf": [1, 2],
            "regressor__max_features": ["sqrt", "log2"]
        }
            grid = GridSearchCV(
            pipeline,
            param_grid,
            cv=3,
            scoring="r2",
            n_jobs=-1,
            verbose=0
        )
            grid.fit(X_train, Y_train)
            self.model = grid.best_estimator_

        preds = self.model.predict(X_test) 
        # evaluation
        return {
            "mae":mean_absolute_error(Y_test,preds),
            "r2":r2_score(Y_test,preds) 
        }
    
    def save(self,path="flight_models/flight_price_model.pkl"):
       joblib.dump(self.model,path)


