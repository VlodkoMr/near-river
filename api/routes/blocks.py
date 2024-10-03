from fastapi import APIRouter, HTTPException
from models.block_model import BlockModel
from services.db_service import DatabaseService

router = APIRouter()

@router.get("/count")
async def count_blocks():
    try:
        async with DatabaseService():
            return await BlockModel.filter().count()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
