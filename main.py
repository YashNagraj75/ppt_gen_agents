import json
import os
import uuid

from fastapi import BackgroundTasks, FastAPI, HTTPException
from google.cloud import batch_v1

from schema import Input

app = FastAPI()

client = batch_v1.BatchServiceClient()
parent = "projects/edunova-455712/locations/asia-south1"


@app.post("/create", status_code=202)
async def create(input: Input, background_tasks: BackgroundTasks):
    doc_id = input.doc_id
    job_name = f"job-{uuid.uuid4().hex}"

    background_tasks.add_task(submit)
    return {"status": "scheduled", "job_name": job_name}


@app.get("/status/{job_name}")
def status(job_name: str):
    job = client.get_job(name=f"{parent}/jobs/{job_name}")
    return {"state": job.status.state.name}
