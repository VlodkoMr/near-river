import logging

from fastapi import FastAPI

from routes import block, transaction, account, analytics
# from services.ai_vector_service import AiVectorService
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

    # Start embedding generation as a background task
    # if conf.ENABLE_AI_PROCESSING:
    #     asyncio.create_task(generate_ai_vectors_process())
    # else:
    #     logger.info("AI processing is disabled, embedding generation will not run.")

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

# ----------------- Background tasks - generate data for AI ----------------

# async def generate_ai_vectors_process(batch_size: int = 1000):
#     while True:
#         try:
#             await AiVectorService().generate_vectors_for_receipt_actions(batch_size=batch_size)
#         except Exception as e:
#             logger.error(f"Error during embedding generation: {e}")
#         await asyncio.sleep(30)  # Wait for 30 second before next cycle

# ------------------- Background tasks - Events Listener -------------------

# async def start_event_listener_process():
#     event_listener = EventListener(
#         smart_contracts=set(),
#         methods=set(),
#         check_interval=10  # Check every 10 seconds
#     )
#     await event_listener.start_listeners()
