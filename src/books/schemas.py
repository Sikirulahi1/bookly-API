from pydantic import BaseModel
import uuid
from datetime import datetime, date

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class CreateBook(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class UpdateBook(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str