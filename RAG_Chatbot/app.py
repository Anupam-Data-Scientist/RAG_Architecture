# app.py

from fastapi import FastAPI, Query
from query_engine import search_and_respond

app = FastAPI()

@app.get("/query")
def query(question: str = Query(..., description="Enter your question")):
    response = search_and_respond(question)
    return {"response": response}
