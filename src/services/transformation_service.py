from fastapi import HTTPException
import pika
import json
import base64
import requests
from src.repositories.transformation_job_repository import TransformationJobRepository
from src.models.transformation_job import TransformationJob, JobStatus
from src.schemas.transformation_job import TransformationJobStatus
from src.core.config import settings

class TransformationService:
    def __init__(self, repository: TransformationJobRepository):
        self.repository = repository

    def _send_to_load_service(self, job_id: int, transformed_data: str):
        url = settings.LOAD_URL

        payload = {
            "job_id": job_id,
            "data": transformed_data
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

    def _callback(self, ch, method, properties, body):
        message = json.loads(body)

        job_id = message["job_id"]
        data = message["data"]

        transformed_data = base64.b64encode(json.dumps(data).encode('utf-8'))

        job = TransformationJob(status=JobStatus.IN_PROGRESS, extraction_job_id=job_id)
        self.repository.add(job)

        try:
            self._send_to_load_service(job.id, transformed_data)
            job.status = JobStatus.COMPLETED
        except Exception:
            job.status = JobStatus.FAILED

        self.repository.update(job)

    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='extraction', exchange_type='direct')
        channel.queue_declare(queue='extraction_queue')
        channel.queue_bind(exchange='extraction', queue='extraction_queue', routing_key='extraction.queue')

        channel.basic_consume(queue='extraction_queue', on_message_callback=self._callback, auto_ack=True)
        print("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    def get_transformation_status(self, job_id: int) -> TransformationJobStatus:
        job = self.repository.get(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return TransformationJobStatus(id=job.id, status=job.status)