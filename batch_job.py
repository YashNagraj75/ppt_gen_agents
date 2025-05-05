import os
import uuid

from google.cloud import batch_v1
from google.cloud.batch_v1.types import (
    AllocationPolicy,
    ComputeResource,
    Job,
    Runnable,
    TaskGroup,
    TaskSpec,
)


async def submit_batch_job(doc_id: str) -> str:
    """
    Submit a Cloud Batch job that runs `agent_loop.py <doc_id> <job_name>`
    inside your worker container, with env‑vars and n1‑f1‑micro resources.
    Returns the job resource name (e.g. projects/.../jobs/job-...).
    """

    client = batch_v1.BatchServiceAsyncClient()

    region = "asia-south1"
    parent = f"projects/edunova-455712/locations/{region}"
    job_id = f"job-{uuid.uuid4().hex}"

    container = Runnable.Container(
        image_uri="asia-south1-docker.pkg.dev/edunova-455712/ppt-gen-agents/worker:latest",
        entrypoint="python",
        commands=["agent_loop.py", doc_id],
    )
    runnable = Runnable(container=container)

    runnable.environment.variables["MONGO_URI"] = str(os.getenv("MONGO_URI"))
    runnable.environment.variables["GEMINI_API_KEY"] = str(os.getenv("GEMINI_API_KEY"))
    runnable.environment.variables["OPENAI_API_KEY"] = str(os.getenv("OPENAI_API_KEY"))
    runnable.environment.variables["CSE_ID"] = str(os.getenv("CSE_ID"))

    compute = ComputeResource(cpu_milli=250, memory_mib=614)

    task_spec = TaskSpec(
        runnables=[runnable],
        compute_resource=compute,
        max_retry_count=1,
        max_run_duration="1800s",
    )
    task_group = TaskGroup(task_spec=task_spec, task_count=1, parallelism=1)

    allocation_policy = batch_v1.AllocationPolicy()
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = "f1-micro"
    instances = batch_v1.AllocationPolicy.InstancePolicyOrTemplate()
    instances.policy = policy
    allocation_policy.instances = [instances]

    job = Job()
    job.task_groups = [task_group]
    job.allocation_policy = allocation_policy
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    response = await client.create_job(
        request={"parent": parent, "job_id": job_id, "job": job}
    )

    return response.name
