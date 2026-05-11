import asyncio
import sys
import os 
from contextlib import asynccontextmanager
if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )
from fastapi import FastAPI
from app.routes.flights import router as flights_router 
@asynccontextmanager
async def lifecycle(app:FastAPI):
    # Startup
    BASE_DIR = "data"
    os.makedirs(BASE_DIR, exist_ok=True)

    app.state.base_dir = BASE_DIR
    app.state.flights_data = []

    print("Application startup complete.")
    yield

    # Shutdown
    print("Application shutdown complete.")
app = FastAPI(lifespan=lifecycle) 

app.include_router(flights_router)