import base64
import json

from fastapi import FastAPI, HTTPException

from Agents.schema import Document
from schema import PubSubPush

app = FastAPI()


@app.get("/ping")
def ping():
    return {"pong"}


@app.post("/create")
async def create(push: PubSubPush):
    # 1) decode the base64 data
    try:
        decoded = base64.b64decode(push.message.data).decode("utf-8")
        payload = json.loads(decoded)
    except Exception as e:
        # invalid Base64 or JSON
        raise HTTPException(status_code=400, detail=f"Invalid message data: {e}")

    # 2) extract your doc_id
    doc_id = payload.get("doc_id")
    if not doc_id:
        raise HTTPException(status_code=400, detail="`doc_id` missing in payload")

    print(f"Received doc_id: {doc_id}")  # now you see it in logs

    # 3) return 200–204 to acknowledge
    return {"status": "ack", "doc_id": doc_id}
