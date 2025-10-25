from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from src.auth.models import User

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column= Column(pg.UUID(), nullable=False, default=uuid.uuid4, primary_key=True)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid"
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow))
    user: Optional["User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, publisher={self.publisher})"