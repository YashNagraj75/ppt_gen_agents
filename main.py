from fastapi import FastAPI

from Agents.schema import Document

app = FastAPI()


@app.get("/ping")
def ping():
    return {"pong"}


@app.post("/create")
def create(document: Document):
    print(f"Received doc_id: {document.doc_id}")
    return {"message": f"Document: {document.doc_id} created and processed"}
