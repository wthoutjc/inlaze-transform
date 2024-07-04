from sqlalchemy.orm import Session
from src.models.transformation_job import TransformationJob

class TransformationJobRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, job: TransformationJob) -> TransformationJob:
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job: TransformationJob) -> TransformationJob:
        self.db.commit()
        self.db.refresh(job)
        return job

    def get(self, job_id: int) -> TransformationJob:
        return self.db.query(TransformationJob).filter(TransformationJob.id == job_id).first()
