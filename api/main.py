import logging

from fastapi import FastAPI

from routes import block, transaction, account, analytics
from services.database_service import DatabaseService

# from services.event_listener_service import EventListener

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------- API Endpoints --------------------------

app = FastAPI(title="NEAR River API")


@app.get("/")
async def root():
    return {"message": "Welcome! Visit /docs for the API documentation."}


app.include_router(block.router, prefix="/block", tags=["blocks"])
app.include_router(transaction.router, prefix="/transaction", tags=["transactions"])
app.include_router(account.router, prefix="/account", tags=["accounts"])
app.include_router(analytics.router, prefix="/analytic", tags=["analytics"])


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
