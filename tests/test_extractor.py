import asyncio
from app.services.extractor import FlightExtractor
from app.services.parsers import FlightParser


async def main():
    extractor = FlightExtractor(headless=False)

    data = await extractor.extract(
        origin="Kathmandu",
        destination="Hong Kong",
        depart_date="2026-05-19"
    )

    print("Flights found:", len(data))
    for flight in data[:3]:
      parsed = FlightParser.parse(flight)
      print(parsed)


asyncio.run(main())