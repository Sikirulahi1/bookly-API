from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel
import uuid
from sqlmodel import Field, Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
if TYPE_CHECKING:
    from src.books.models import Book



class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column= Column(pg.UUID(), nullable=False, default=uuid.uuid4, primary_key=True)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR(length=20), nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow))
    books: list["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})


    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"