from fastapi import APIRouter, HTTPException

from models.block_model import BlockModel
from services.db_service import DatabaseService

router = APIRouter()

@router.get("/analytics/test")
async def execute_analytics(id: int):
    try:
        async with DatabaseService():
            block = await BlockModel.get(block_height=id)
            print('block', block)
            return block

        # result = await execute_saved_analytics(id)
        # return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
