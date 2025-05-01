from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def ping():
    return {"pong"}


@app.post("/create")
def create():
    return {"message": "Document created and processed"}
