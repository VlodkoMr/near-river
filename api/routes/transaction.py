from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from config.settings import conf
from helpers.decorators import exception_handler
from models.transaction_model import TransactionModel
from services.database_service import DatabaseService

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
        limit = conf.DEFAULT_PAGE_LIMIT
        query = """
            SELECT DATE(block_timestamp) AS date, COUNT(*) AS transaction_count 
            FROM transactions 
            GROUP BY date 
            ORDER BY date DESC
            LIMIT $1
        """
        return await db.run_raw_sql(query, [limit])


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
        limit: Optional[int] = conf.DEFAULT_PAGE_LIMIT,
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


@router.get("/tx-sent/{signer_id}")
@exception_handler
async def get_tx_by_signer_id(
        signer_id: str,
        limit: Optional[int] = conf.DEFAULT_PAGE_LIMIT,
        offset: Optional[int] = 0
):
    """ Get transactions sent by the account """
    async with DatabaseService():
        total_records = await TransactionModel.filter(signer_id=signer_id).count()
        paginated_result = await TransactionModel.filter(
            signer_id=signer_id
        ).order_by("block_timestamp") \
            .offset(offset) \
            .limit(limit) \
            .all()

        return {
            "total": total_records,
            "result": paginated_result
        }


@router.get("/tx-received/{receiver_id}")
@exception_handler
async def get_tx_by_receiver_id(
        receiver_id: str,
        limit: Optional[int] = conf.DEFAULT_PAGE_LIMIT,
        offset: Optional[int] = 0
):
    """ Get transactions received by the account """
    async with DatabaseService():
        total_records = await TransactionModel.filter(receiver_id=receiver_id).count()
        paginated_result = await TransactionModel.filter(
            receiver_id=receiver_id
        ).order_by("block_timestamp") \
            .offset(offset) \
            .limit(limit) \
            .all()

        return {
            "total": total_records,
            "result": paginated_result
        }
