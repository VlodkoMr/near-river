from typing import Optional
from fastapi import APIRouter, HTTPException

from config import conf
from helpers.decorators import exception_handler
from models.transaction_model import TransactionModel
from services.db_service import DatabaseService

router = APIRouter()


@router.get("/tx-signer/{signer_id}")
@exception_handler
async def get_tx_by_signer_id(
        signer_id: str,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    async with DatabaseService():
        total_records = await TransactionModel.filter(signer_id=signer_id).count()

        # Get the paginated result
        paginated_result = await TransactionModel.filter(
            signer_id=signer_id
        ).order_by("block_timestamp") \
            .offset(offset) \
            .limit(limit) \
            .all()

        # Return total count and current page result
        return {
            "total": total_records,
            "result": paginated_result
        }


@router.get("/tx-receiver/{receiver_id}")
@exception_handler
async def get_tx_by_receiver_id(
        receiver_id: str,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    async with DatabaseService():
        total_records = await TransactionModel.filter(receiver_id=receiver_id).count()

        # Get the paginated result
        paginated_result = await TransactionModel.filter(
            receiver_id=receiver_id
        ).order_by("block_timestamp") \
            .offset(offset) \
            .limit(limit) \
            .all()

        # Return total count and current page result
        return {
            "total": total_records,
            "result": paginated_result
        }
