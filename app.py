# uvicorn app:app --host 0.0.0.0 --port 5001 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.transformation import router
from src.core.config import settings
import logging
from threading import Thread
from src.database.database import Database
from src.repositories.transformation_job_repository import TransformationJobRepository
from src.services.transformation_service import TransformationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ETL Extraction Microservice")

app.include_router(router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def start_transformation_service():
    db_instance = Database.get_instance().get_db()
    repository = TransformationJobRepository(db_instance)
    service = TransformationService(repository)
    service.start()

transformation_thread = Thread(target=start_transformation_service)
transformation_thread.start()