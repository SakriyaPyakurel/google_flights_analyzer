# ✈️ Google Flights Analyzer

> A FastAPI-powered flight data extraction, analytics, and machine learning platform built using Google Flights, Playwright, Pandas, and Scikit-Learn.


# 📌 Project Overview

Google Flights Analyzer is an end-to-end flight data platform that:

✅ Extracts flight information from Google Flights using Playwright

✅ Parses and structures raw flight information

✅ Stores flight datasets in memory and CSV files

✅ Performs feature engineering for machine learning

✅ Trains flight price prediction models

✅ Supports quick in-memory model training

✅ Supports persistent model saving via Pickle (.pkl)

✅ Prepares data for advanced visualizations and dashboards

---

# 🚀 Features

## 🔍 Flight Extraction

Extract flight details directly from Google Flights including:

- Origin
- Destination
- Airline
- Price
- Number of Stops
- Departure Airport
- Arrival Airport
- Departure Time
- Arrival Time
- Duration
- Transit Airports
- Transit Durations

Powered by:

- Playwright
- Chromium Browser
- FastAPI

---

## 📊 Flight Data Processing

Raw flight descriptions are automatically parsed into structured records.

Example:

```json
{
    "origin": "Kathmandu",
    "destination": "Hong Kong",
    "airline": "Cathay Pacific",
    "stops": 0,
    "departure_time": "11:00 PM",
    "arrival_time": "6:00 AM",
    "duration_minutes": 285,
    "price": 167008
}
```

---

## 💾 CSV Export System

Flight data can be:

- Stored in FastAPI App State
- Exported to CSV
- Appended to existing CSV files
- Overwritten if requested

Supported Options:

| Option | Description |
|----------|----------|
| override=True | Replace existing file |
| override=False | Append new records |
| pathname | Custom save location |

---

## ⚡ FastAPI State Management

Instead of immediately writing every extraction to disk, flight records are maintained in:

```python
app.state.flights_data
```

Benefits:

- Faster access
- Temporary storage
- Quick model training
- Reduced disk I/O

---

## 🧠 Machine Learning Module

Train a flight price prediction model directly through API endpoints.

Two training modes:

### Mode 1: State-Based Training

Uses:

```python
app.state.flights_data
```

Advantages:

✅ Fast

✅ No file generation

✅ Useful for experimentation

Model stored in:

```python
app.state.flight_quick_model
```

---

### Mode 2: CSV-Based Training

Uses:

```python
flight_data.csv
```

Advantages:

✅ Persistent dataset

✅ Reproducible training

✅ Saves trained model automatically

Produces:

```text
models/
└── flight_price_model.pkl
```

---

# 🔧 Feature Engineering

The following transformations are performed before training:

### Date Features

Extract:

- Departure Month
- Departure Day
- Return Month
- Return Day

### Route Features

Encode:

- Origin
- Destination
- Airports

### Airline Features

Encode:

- Airline Name

### Flight Features

- Stops
- Duration Minutes
- Departure Time
- Arrival Time

Target Variable:

```python
price
```

---

# 📈 Planned Visualizations

The project includes a dedicated Jupyter Notebook workflow for Exploratory Data Analysis.

### Flight Pricing

📊 Average Price by Airline

📊 Average Price by Route

📊 Cheapest Destinations

📊 Most Expensive Routes

---

### Flight Duration Analysis

📊 Duration Distribution

📊 Stops vs Duration

📊 Duration vs Price

---

### Airport Analysis

📊 Most Frequent Airports

📊 Most Popular Routes

📊 Transit Airport Frequency

---

### Time-Based Analysis

📊 Monthly Pricing Trends

📊 Departure Time Distribution

📊 Return Date Analysis

---

# 🏗 Project Structure

```text
google_flights_analyzer/
│
├── app/
│   │
│   ├── routes/
│   │   ├── flights.py
│   │   └── ml.py
│   │
│   ├── services/
│   │   ├── extractor.py
│   │   ├── parsers.py
│   │   ├── feature_engineering.py
│   │   └── model_trainer.py
│   │
│   ├── models/
│   │   ├── flight_schema.py
│   │   └── flight_ml_schema.py
│   │
│   └── main.py
│
├── data/
│
├── outputs/
│
├── models/
│
├── notebooks/
│   └── analysis.ipynb
│
├── tests/
│   └── test_extractor.py
│
├── requirements.txt
│
└── README.md
```

---

# 🌐 API Endpoints

## Search Flights

```http
POST /flights/search
```

Request:

```json
{
    "origin": "Kathmandu",
    "destination": "Hong Kong",
    "depart_date": "2026-05-19",
    "return_date": "2026-06-16"
}
```

---

## Raw Flight Stream

```http
POST /flights/text_streamer
```

Returns unprocessed Google Flights descriptions.

---

## Save Flights To CSV

```http
POST /flights/flights_save_to_csv
```

Request:

```json
{
    "pathname": "flights.csv",
    "override": false
}
```

---

## Train Machine Learning Model

```http
POST /ml/train
```

Training From State:

```json
{
    "source": "state"
}
```

Training From CSV:

```json
{
    "source": "csv",
    "csv_path": "data/flights.csv",
    "pkl_path": "flight_price_model.pkl"
}
```

---

# ⚙️ Installation

Clone Repository

```bash
git clone https://github.com/SakriyaPyakurel/google_flights_analyzer.git
cd google_flights_analyzer
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Install Playwright Browser

```bash
playwright install chromium
```

Run Server

```bash
uvicorn app.main:app
```

Swagger UI: http://127.0.0.1:8000/docs


---

# 🛠 Technologies Used

### Backend

- FastAPI
- Uvicorn

### Data Collection

- Playwright
- Chromium

### Data Processing

- Pandas
- NumPy
- Regex

### Machine Learning

- Scikit-Learn
- Joblib

### Visualization

- Matplotlib
- Seaborn
- Jupyter Notebook

### Future Dashboard

- Streamlit

---

# 🎯 Future Enhancements

### Phase 1

- Route popularity prediction
- Cheapest flight finder
- Price trend forecasting

### Phase 2

- Interactive Streamlit Dashboard
- Airline comparison dashboard
- Route comparison dashboard

### Phase 3

- Automated scheduled scraping
- Historical price database
- Advanced ML models
- Flight recommendation system

---

# 📚 Learning Goals

This project was created to strengthen practical skills in:

✅ FastAPI Development

✅ Web Scraping with Playwright

✅ Data Engineering

✅ Exploratory Data Analysis

✅ Feature Engineering

✅ Machine Learning Pipelines

✅ Model Deployment

✅ API Design

---

# ⭐ Author

**Sakriya Pyakurel**

Passionate about:

✈️ Flight Analytics

📊 Data Science

🤖 Machine Learning

⚡ FastAPI Development

🌐 Real-world Data Engineering Projects

---

## Feedbacks and recommendations will be appreciated.😊

*"Turning flight data into actionable insights."* ✈️📈