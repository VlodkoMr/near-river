from fastapi import APIRouter, HTTPException
from schemas.query_schema import QueryCreate
from services.task_service import save_new_task, execute_saved_query, get_all_tasks

router = APIRouter()

@router.post("/save-task")
async def create_task(task_data: QueryCreate):
    try:
        return await save_new_task(task_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not save task: {str(e)}")

@router.get("/execute-query/{id}")
async def execute_query(id: int):
    try:
        return await execute_saved_query(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving query: {str(e)}")

@router.get("/get-tasks")
async def list_tasks():
    try:
        return await get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving tasks: {str(e)}")
