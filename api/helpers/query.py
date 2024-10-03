from fastapi import HTTPException
from services.db_service import DatabaseService

async def run_query(db_service: DatabaseService, query: str):
    """Run SQL query and return result."""
    try:
        pass
        # with db_service.get_session() as db:
        #     result = db.execute(text(query))
        #     return [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query failed: {str(e)}")