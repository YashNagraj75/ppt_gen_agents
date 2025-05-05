from fastapi import FastAPI
from google.cloud import batch_v1

from batch_job import submit_batch_job
from schema import Input

app = FastAPI()

client = batch_v1.BatchServiceClient()


@app.post("/create", status_code=202)
async def create(input: Input):
    doc_id = input.doc_id
    print(f"Received doc_id: {doc_id}")
    job_name = await submit_batch_job(doc_id)
    return {"status": "scheduled", "job_name": job_name}


@app.get("/status/{job_name}")
def status(job_name: str):
    job = client.get_job(name=f"edunova-455712/jobs/{job_name}")
    return {"state": job.status.state.name}
