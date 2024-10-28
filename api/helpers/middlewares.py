import os
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_SECRET_KEY = os.getenv("API_SECRET_KEY")
API_KEY_HEADER = APIKeyHeader(name="x-api-key", auto_error=False)


async def api_key_check(api_key: str = Security(API_KEY_HEADER)):
    if API_SECRET_KEY and api_key == API_SECRET_KEY:
        return True
    elif not API_SECRET_KEY:  # No API key set, allow public access
        return True
    raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

