from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting up...")
    await init_db()
    yield
    print("Server is shutting down...")

version = "v1"

app = FastAPI(
    title="Bookly API",
    description="An API for a book review web service",
    version=version,
    lifespan=lifespan
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])