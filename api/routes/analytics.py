from fastapi import APIRouter, HTTPException
from services.analytics_service import execute_saved_analytics

router = APIRouter()

@router.get("/execute-analytics/{id}")
async def execute_analytics(id: int):
    try:
        return await execute_saved_analytics(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving analytics task: {str(e)}")
