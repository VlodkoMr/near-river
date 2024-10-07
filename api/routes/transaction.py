from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException

from config import conf
from helpers.decorators import exception_handler
from models.transaction_model import TransactionModel
from services.db_service import DatabaseService

router = APIRouter()


@router.get("/count")
@exception_handler
async def count_tx():
    async with DatabaseService():
        return await TransactionModel.filter().count()


@router.get("/daily-count")
@exception_handler
async def get_transaction_daily_count():
    async with DatabaseService() as db:
        return await db.run_raw_sql(
            query="SELECT DATE(block_timestamp) AS date, COUNT(*) AS transaction_count FROM transactions GROUP BY date ORDER BY date"
        )


@router.get("/daily-volume")
@exception_handler
async def get_transaction_daily_volume():
    async with DatabaseService() as db:
        return await db.run_raw_sql(
            query="SELECT DATE(block_timestamp) AS date, SUM(deposit) AS volume FROM receipt_actions GROUP BY date ORDER BY date"
        )


@router.get("/hash/{hash}")
@exception_handler
async def get_tx_by_hash(hash: str):
    async with DatabaseService():
        transaction = await TransactionModel.filter(tx_hash=hash).first()
        if transaction:
            return transaction
        raise HTTPException(status_code=404, detail="Transaction not found")


@router.get("/block/{height}")
@exception_handler
async def get_tx_by_block_height(height: int):
    async with DatabaseService():
        return await TransactionModel.filter(block_height=height).all()


@router.get("/timestamp-range")
@exception_handler
async def get_tx_by_timestamp_range(
        start: int,
        end: int,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    # Convert Unix timestamp (int) to datetime
    start_datetime = datetime.fromtimestamp(start)
    end_datetime = datetime.fromtimestamp(end)

    async with DatabaseService():
        total_records = await TransactionModel.filter(
            block_timestamp__gte=start_datetime,
            block_timestamp__lte=end_datetime
        ).count()

        # Get the paginated result
        paginated_result = await TransactionModel.filter(
            block_timestamp__gte=start_datetime,
            block_timestamp__lte=end_datetime
        ).order_by("block_timestamp") \
            .offset(offset) \
            .limit(limit) \
            .all()

        # Return total count and current page result
        return {
            "total": total_records,
            "result": paginated_result
        }
