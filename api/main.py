from fastapi import FastAPI
from routes import tasks, analytics

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Near Watch API"}

# Routers
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])


