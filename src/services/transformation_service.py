from fastapi import HTTPException
import pika
import json
from sqlalchemy.orm import Session
from src.models.transformation_job import TransformationJob, JobStatus
from src.repositories.transformation_job_repository import TransformationJobRepository
from src.schemas.transformation_job import TransformationJobCreate, TransformationJobStatus

class TransformationService:
    def __init__(self, repository: TransformationJobRepository):
        self.repository = repository

    def start_transformation(self, job_data: TransformationJobCreate, db: Session) -> TransformationJobStatus:
        job = TransformationJob(
            extraction_job_id=job_data.extraction_job_id,
            status=JobStatus.IN_PROGRESS
        )
        job = self.repository.add(job)

        # Lógica de transformación aquí
        try:
            # Consumir los datos del mensaje de RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            def callback(ch, method, properties, body):
                data = json.loads(body)
                # Procesar los datos aquí
                # Actualizar el estado del trabajo
                job.status = JobStatus.COMPLETED
                self.repository.update(job)

            channel.basic_consume(queue='extraction_queue', on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        except Exception:
            job.status = JobStatus.FAILED
            self.repository.update(job)

        return TransformationJobStatus(id=job.id, status=job.status)

    def get_transformation_status(self, job_id: int, db: Session) -> TransformationJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return TransformationJobStatus(id=job.id, status=job.status)
