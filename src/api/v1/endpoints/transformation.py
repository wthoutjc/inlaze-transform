from fastapi import APIRouter, Depends
from src.schemas.transformation_job import TransformationJobStatus
from src.services.transformation_service import TransformationService
from src.database.database import Database
from sqlalchemy.orm import Session
from src.services.transformation_service import TransformationService
from src.repositories.transformation_job_repository import TransformationJobRepository

router = APIRouter()

def get_db():
    db = Database.get_instance().get_db()
    try:
        yield db
    finally:
        Database.get_instance().close_db()

def get_transformation_service(db: Session = Depends(get_db)) -> TransformationService:
    repository = TransformationJobRepository(db)
    return TransformationService(repository)


@router.get("/transform/status/{job_id}", response_model=TransformationJobStatus)
def get_transformation_status(
    job_id: int,
    transformation_service: TransformationService = Depends(get_transformation_service)
):
    return transformation_service.get_transformation_status(job_id)
