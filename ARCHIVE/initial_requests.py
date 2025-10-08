from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/greet")
async def greet(name: Optional[str] = "User", age: Optional[int] = 0) -> dict:
    return {"message": f"Hello, {name}!", "age":age}


class BookCreateModel(BaseModel):
    title: str
    author: str

 

@app.post('/create_book')
async def create_book(book_data: BookCreateModel) -> dict:
    return {
        "title": book_data.title,
        "author": book_data.author,
    }

@app.get("/get_headers", status_code=200)
async def get_headers(
    accept:str = Header(None),
    content_type:str = Header(None),
    user_agent:str = Header(None),
    host:str = Header(None)
):
    request_headers = {}

    request_headers["accept"] = accept
    request_headers["content_type"] = content_type
    request_headers["user_agent"] = user_agent
    request_headers["host"] = host

    return request_headers