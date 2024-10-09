import asyncio
import logging

from fastapi import FastAPI

from config import conf
from routes import block, transaction, account
from services.ai_vector_service import AiVectorService
from services.db_service import DatabaseService

app = FastAPI(title="NEAR River API")
ai_vector_service = AiVectorService()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Welcome! Visit /docs for the API documentation."}


# API Routers
app.include_router(block.router, prefix="/block", tags=["blocks"])
app.include_router(transaction.router, prefix="/transaction", tags=["transactions"])
app.include_router(account.router, prefix="/account", tags=["accounts"])


@app.on_event("startup")
async def startup_event():
    db_service = await DatabaseService.initialize()

    # Start embedding generation as a background tasks
    if conf.ENABLE_AI_PROCESSING:
        asyncio.create_task(generate_ai_vectors_process())
    else:
        logger.info("AI processing is disabled, embedding generation will not run.")


@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections
    await DatabaseService.shutdown()
    logger.info("Database connections closed.")


# --------------- Background task - generate vector data for AI ---------------

async def generate_ai_vectors_process(batch_size: int = 1000):
    while True:
        try:
            await ai_vector_service.generate_vectors_for_receipt_actions(batch_size=batch_size)
        except Exception as e:
            logger.error(f"Error during embedding generation: {e}")
        await asyncio.sleep(30)  # Wait for 30 second before next cycle
