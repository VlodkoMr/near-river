import pandas as pd
import dask.dataframe as dd
from sqlalchemy import text
from fastapi import HTTPException
from services.db_service import DatabaseService

async def execute_saved_analytics(id: int):
    query = "SELECT task FROM tasks WHERE id = :id AND task_type = 'analytics'"

    db_service = DatabaseService()
    with db_service.get_session() as db:
        result = db.execute(text(query), {"id": id}).fetchone()
        if result:
            pass
        else:
            raise HTTPException(status_code=404, detail="Analytics task not found")
