from fastapi import FastAPI

from agent import process_query
from schema import ChatQuery

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/query")
async def query(data: ChatQuery):
    user_query = data.query
    return process_query(
        user_query,
        "You are an expert data analyst. Generate the appropriate SQL query for the user's request. Follow these guidelines:",
    )
