from fastapi import FastAPI
from routes import analytics, blocks, transactions

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Near Watch API"}

# Routers
app.include_router(blocks.router, prefix="/blocks", tags=["blocks"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
