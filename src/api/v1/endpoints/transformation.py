from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.transformation_job import TransformationJobCreate, TransformationJobStatus
from src.services.transformation_service import TransformationService
from src.repositories.transformation_job_repository import TransformationJobRepository
from src.database.session import get_db

router = APIRouter()

def get_transformation_service(db: Session = Depends(get_db)) -> TransformationService:
    repository = TransformationJobRepository(db)
    return TransformationService(repository)

@router.post("/transform", response_model=TransformationJobStatus)
def start_transformation(
    job: TransformationJobCreate,
    db: Session = Depends(get_db),
    transformation_service: TransformationService = Depends(get_transformation_service)
):
    return transformation_service.start_transformation(job, db)

@router.get("/transform/status/{job_id}", response_model=TransformationJobStatus)
def get_transformation_status(
    job_id: int,
    db: Session = Depends(get_db),
    transformation_service: TransformationService = Depends(get_transformation_service)
):
    return transformation_service.get_transformation_status(job_id, db)
