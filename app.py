from fastapi import FastAPI
from src.api.v1.endpoints.transformation import router as transformation_router
from src.database.session import engine
from src.database.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transformation_router, prefix="/api/v1")