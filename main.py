import base64
import json
import logging

from fastapi import BackgroundTasks, FastAPI, HTTPException

from agent_loop import main
from schema import PubSubPush

app = FastAPI()

logger = logging.getLogger("ppt_processor")
logger.setLevel(logging.INFO)


async def process_ppt(doc_id: str):
    try:
        logger.info(f"✔️ Starting processing for doc_id: {doc_id}")
        await main(doc_id)  # your real work
        logger.info(f"Finished processing for doc_id: {doc_id}")
    except Exception:
        logger.exception(f"Failed processing for doc_id: {doc_id}")


@app.get("/ping")
def ping():
    return {"pong"}


@app.post("/create")
async def create(push: PubSubPush, background_tasks: BackgroundTasks):
    try:
        decoded = base64.b64decode(push.message.data).decode("utf‑8")
        payload = json.loads(decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid message data: {e}")

    doc_id = payload.get("doc_id")
    if not doc_id:
        raise HTTPException(status_code=400, detail="`doc_id` missing in payload")

    background_tasks.add_task(process_ppt, doc_id)

    return {"status": "acknowledged", "doc_id": doc_id}
