from functools import wraps
from fastapi import HTTPException

def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
    return wrapper
