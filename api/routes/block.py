from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from config.settings import conf
from helpers.decorators import exception_handler
from models.block_model import BlockModel
from services.database_service import DatabaseService

router = APIRouter()


@router.get("/timestamp-range")
@exception_handler
async def get_blocks_by_timestamp_range(
        start: int,
        end: int,
        limit: Optional[int] = conf.PAGE_LIMIT,
        offset: Optional[int] = 0
):
    # Convert Unix timestamp (int) to datetime
    start_datetime = datetime.fromtimestamp(start)
    end_datetime = datetime.fromtimestamp(end)

    async with DatabaseService():
        # Get the total number of records (without pagination)
        total_records = await BlockModel.filter(
            block_timestamp__gte=start_datetime,
            block_timestamp__lte=end_datetime
        ).count()

        # Get the paginated result
        paginated_result = await BlockModel.filter(
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


@router.get("/{height}")
@exception_handler
async def block_by_height(height: int):
    async with DatabaseService():
        block = await BlockModel.filter(block_height=height).first()
        if block:
            return block
        raise HTTPException(status_code=404, detail="Block not found")
