import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )
from fastapi import FastAPI
from app.routes.flights import router as flights_router 

app = FastAPI() 
app.include_router(flights_router)