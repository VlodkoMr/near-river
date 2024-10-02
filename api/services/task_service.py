from sqlalchemy import text
from fastapi import HTTPException

from helpers.query import run_query
from schemas.query_schema import QueryCreate
from services.db_service import DatabaseService

db_service = DatabaseService()

async def save_new_task(task_data: QueryCreate):
    query = "INSERT INTO tasks (name, task_type, task) VALUES (:name, :task_type, :task)"

    with db_service.get_session() as db:
        db.execute(text(query), {"name": task_data.name, "task_type": task_data.task_type, "task": task_data.task})
    return {"message": "Task saved successfully"}

async def execute_saved_query(id: int):
    query = "SELECT task FROM tasks WHERE id = :id AND task_type = 'query'"

    with db_service.get_session() as db:
        result = db.execute(text(query), {"id": id}).fetchone()
        if result:
            return await run_query(db_service, result[0])
        else:
            raise HTTPException(status_code=404, detail="Query not found")

async def get_all_tasks():
    query = "SELECT id, name, task_type FROM tasks"

    with db_service.get_session() as db:
        result = db.execute(text(query)).fetchall()
        return [{"id": row["id"], "name": row["name"], "task_type": row["task_type"]} for row in result]

