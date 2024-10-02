from pydantic import BaseModel
from typing import Optional

class QueryCreate(BaseModel):
    name: Optional[str] = None
    task_type: str
    task: str
