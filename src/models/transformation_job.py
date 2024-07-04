from sqlalchemy import Column, Integer, String, Enum
from src.database.base import Base
from enum import Enum as PyEnum

class JobStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TransformationJob(Base):
    __tablename__ = "transformation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    extraction_job_id = Column(Integer, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)