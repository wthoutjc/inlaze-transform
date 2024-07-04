from pydantic import BaseModel
from enum import Enum

class JobStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TransformationJobCreate(BaseModel):
    extraction_job_id: int
    # Otros campos relevantes

class TransformationJobStatus(BaseModel):
    id: int
    status: JobStatusEnum