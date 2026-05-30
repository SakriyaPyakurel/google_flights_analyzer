from playwright.async_api import async_playwright
from urllib.parse import quote
import asyncio
class FlightExtractor:
    def __init__(self,headless:bool = True):
        self.headless = headless 
        self._responses = [] 
    def _build_google_flights_url(self,origin, destination, depart_date, return_date=None):
      base = "https://www.google.com/travel/flights/search?"
      if return_date:
        query = f"Flights from {origin} to {destination} on {depart_date} returning {return_date}"
      else:
        query = f"Flights from {origin} to {destination} on {depart_date}"
      return base + "q=" + quote(query)
    async def extract(self,origin,destination,depart_date,return_date=None):
       url = self._build_google_flights_url(origin,destination,depart_date,return_date) 
       flight_texts = [] 
       async with async_playwright() as p:
          browser = await p.chromium.launch(
             headless = self.headless,
             args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ],
          )
          context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            )
          page = await context.new_page()
          await page.goto(url,timeout=60000) 
          # waiting for flight results to appear
          await page.wait_for_selector("div[aria-label]",timeout=15000) 
          #scrolling to load more results 
          for _ in range(5):
             await page.mouse.wheel(0,3000) 
             await asyncio.sleep(1.5) 
          #extracting flight info
          cards = await page.locator("div[aria-label]").all()
          for card in cards:
             aria = await card.get_attribute("aria-label",timeout=2000) 
             if not aria:
                continue
             text = aria.lower()
             if (
               "flight" in text and
               ("depart" in text or "arrive" in text or "duration" in text)
               ):
               flight_texts.append(aria)
          await browser.close()
       return flight_texts

