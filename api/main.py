import asyncio
import logging

from fastapi import FastAPI, Depends, HTTPException, Security

from config.settings import conf
from helpers.middlewares import api_key_check
from routes import block, transaction, account, analytics
from services.database_service import DatabaseService
from services.event_subscription_service import EventSubscriptionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------- API Endpoints --------------------------

app = FastAPI(title="NEAR River API")

@app.get("/", dependencies=[Depends(api_key_check)])
async def root():
    return {"message": "Welcome! Visit /docs for the API documentation."}

app.include_router(
    block.router,
    prefix="/block",
    dependencies=[Depends(api_key_check)],
    tags=["blocks"]
)
app.include_router(
    transaction.router,
    prefix="/transaction",
    dependencies=[Depends(api_key_check)],
    tags=["transactions"]
)
app.include_router(
    account.router,
    prefix="/account",
    dependencies=[Depends(api_key_check)],
    tags=["accounts"]
)
app.include_router(
    analytics.router,
    prefix="/analytic",
    dependencies=[Depends(api_key_check)],
    tags=["analytics"]
)

# ------------------------ Start/Stop process ------------------------

@app.on_event("startup")
async def startup_event():
    await DatabaseService.initialize()

    # Start event listeners as a background task
    if conf.ENABLE_EVENT_LISTENER:
        asyncio.create_task(start_event_listener_process())
        logger.info("Embedding and event listener services started.")
    else:
        logger.info("Event listener is disabled.")


@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections
    await DatabaseService.shutdown()
    logger.info("Database connections closed.")

# ------------------- Background tasks - Events Listener -------------------

async def start_event_listener_process():
    # Check every 10 seconds for new transactions and receipt actions
    event_listener = EventSubscriptionService(check_interval=10)
    await event_listener.start_listeners()
