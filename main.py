import base64
import json

from fastapi import FastAPI, HTTPException

from agent_loop import main
from schema import PubSubPush

app = FastAPI()


@app.get("/ping")
def ping():
    return {"pong"}


@app.post("/create")
async def create(push: PubSubPush):
    try:
        decoded = base64.b64decode(push.message.data).decode("utf-8")
        payload = json.loads(decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid message data: {e}")

    doc_id = payload.get("doc_id")
    if not doc_id:
        raise HTTPException(status_code=400, detail="`doc_id` missing in payload")

    success = main(doc_id)
    return {"status": success}
