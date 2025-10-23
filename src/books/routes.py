from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from src.books.schemas import Book, UpdateBook, CreateBook
from .service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
security = AccessTokenBearer()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

@book_router.get("/", response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_all_books(session: AsyncSession = Depends(get_session), user_details=Depends(security)) -> List[dict]:
    print(user_details)
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[Depends(role_checker)])
async def create_a_book(book_data: CreateBook, session: AsyncSession = Depends(get_session), user_details=Depends(security)) -> dict:
    new_book = await book_service.create_book(session, book_data)
    return new_book

@book_router.get("/{book_uid}", response_model=Book, dependencies=[Depends(role_checker)])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(security)) -> dict:
    book = await book_service.get_book(session, book_uid)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@book_router.patch("/{book_uid}", response_model=Book, dependencies=[Depends(role_checker)])
async def update_book(book_uid: str, book_update_data: UpdateBook, session: AsyncSession = Depends(get_session), user_details=Depends(security)) -> dict:
    updated_book = await book_service.update_book(session, book_uid, book_update_data)
    if updated_book:
        return updated_book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(role_checker)])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(security)) -> None:
    deleted_book = await book_service.delete_book(session, book_uid)
    if deleted_book:
        return
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
