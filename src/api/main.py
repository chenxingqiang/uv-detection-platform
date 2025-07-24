from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint to check API status.
    """
    return {"message": f"Welcome to the {settings.APP_NAME}"}

# Future API versions will be included here
# from src.api.v1.endpoints import router as api_router_v1
# app.include_router(api_router_v1, prefix=settings.API_V1_STR)
