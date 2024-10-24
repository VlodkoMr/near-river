import os
import logging

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from routes import block, transaction, account, analytics
from services.database_service import DatabaseService

# from services.event_listener_service import EventListener

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------- API Endpoints --------------------------

app = FastAPI(title="NEAR River API")

API_SECRET_KEY = os.getenv("API_SECRET_KEY")
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def api_key_check(api_key: str = Security(api_key_header)):
    if API_SECRET_KEY and api_key == API_SECRET_KEY:
        return True
    elif not API_SECRET_KEY:  # No API key set, allow public access
        return True
    raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

@app.get("/", dependencies=[Depends(api_key_check)])
async def root():
    return {"message": "Welcome! Visit /docs for the API documentation."}


app.include_router(block.router, prefix="/block", dependencies=[Depends(api_key_check)], tags=["blocks"])
app.include_router(transaction.router, prefix="/transaction", dependencies=[Depends(api_key_check)], tags=["transactions"])
app.include_router(account.router, prefix="/account", dependencies=[Depends(api_key_check)], tags=["accounts"])
app.include_router(analytics.router, prefix="/analytic", dependencies=[Depends(api_key_check)], tags=["analytics"])


# ------------------------ Start/Stop process ------------------------

@app.on_event("startup")
async def startup_event():
    await DatabaseService.initialize()

    # Start event listeners as a background task
    # if conf.ENABLE_EVENT_LISTENER:
    #     asyncio.create_task(start_event_listener_process())
    #     logger.info("Embedding and event listener services started.")
    # else:
    #     logger.info("Event listener is disabled.")


@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections
    await DatabaseService.shutdown()
    logger.info("Database connections closed.")

# ------------------- Background tasks - Events Listener -------------------

# async def start_event_listener_process():
#     event_listener = EventListener(
#         smart_contracts=set(),
#         methods=set(),
#         check_interval=10  # Check every 10 seconds
#     )
#     await event_listener.start_listeners()
