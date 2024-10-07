from fastapi import FastAPI
from routes import block, transaction, account

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome! Visit /docs for the API documentation."}


# Routers
app.include_router(block.router, prefix="/block", tags=["blocks"])
app.include_router(transaction.router, prefix="/transaction", tags=["transactions"])
app.include_router(account.router, prefix="/account", tags=["accounts"])
