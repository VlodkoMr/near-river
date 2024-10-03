from fastapi import APIRouter, HTTPException
from models.transaction_model import TransactionModel
from services.db_service import DatabaseService

router = APIRouter()

@router.get("/count")
async def count_transactions():
    try:
        async with DatabaseService():
            return await TransactionModel.filter().count()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
