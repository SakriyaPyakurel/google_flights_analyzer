import re
from datetime import datetime
def clean_time(t):
    if not t:
        return None 
    return t.replace("\u202f", " ").strip()
class FlightParser:
    @staticmethod
    def parse(text: str) -> dict:
        data = {}

        price_match = re.search(r"From (\d+)", text)
        data["price"] = int(price_match.group(1)) if price_match else None

        if "Nepalese rupees" in text:
            data["currency"] = "NPR"
        else:
            data["currency"] = "USD"

        if "Nonstop" in text:
            data["stops"] = 0
        else:
            stop_match = re.search(r"(\d+) stop", text)
            data["stops"] = int(stop_match.group(1)) if stop_match else None

        airline_match = re.search(r"flight with ([^.]+)", text)
        data["airline"] = airline_match.group(1).strip() if airline_match else None

        dep_match = re.search(r"Leaves .*? at ([0-9:\u202fAPMapm]+)", text)
        data["departure_time"] = clean_time(dep_match.group(1)) if dep_match else None

        arr_match = re.search(r"arrives .*? at ([0-9:\u202fAPMapm]+)", text)
        data["arrival_time"] = clean_time(arr_match.group(1)) if arr_match else None

        dur_match = re.search(r"Total duration ([^.]+)", text)
        data["duration"] = dur_match.group(1) if dur_match else None

        dep_airport = re.search(r"Leaves (.*?) at", text)
        data["departure_airport"] = dep_airport.group(1) if dep_airport else None

        arr_airport = re.search(r"arrives at (.*?) at", text)
        data["arrival_airport"] = arr_airport.group(1) if arr_airport else None

        layover_durations = re.findall(r"(\d+\s*hr\s*\d+\s*min)\s+layover", text)
        layover_airports = re.findall(r"layover at ([^.]+?) in", text)

        data["layover_durations"] = layover_durations or []
        data["layover_airports"] = layover_airports or []

        data["scrape_time"] = datetime.now().strftime("%Y-%m-%d")

        return data