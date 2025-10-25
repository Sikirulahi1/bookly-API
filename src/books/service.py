from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CreateBook, UpdateBook
from sqlmodel import select, desc
from .models import Book
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_user_books(self, session: AsyncSession, user_uid: str):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, session: AsyncSession, book_uid: str):
        statement = select(Book).where(Book.uid == book_uid)
        book = await session.exec(statement)
        result = book.first()
        return result if result is not None else None

    async def create_book(self, session: AsyncSession, create_book: CreateBook, user_uid: str = None):
        create_data_dict = create_book.model_dump()
        new_book = Book(**create_data_dict)

        new_book.published_date = datetime.strptime(create_book.published_date, "%Y-%m-%d")
        if user_uid:
            new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return new_book
        

    async def update_book(self, session: AsyncSession, book_uid: str, update_data: UpdateBook):
        book_update = await self.get_book(session, book_uid)

        update_data_dict = update_data.model_dump()
        if book_update is not None:
            for key, value in update_data_dict.items():
                setattr(book_update, key, value)

        session.add(book_update)
        await session.commit()
        return book_update


    async def delete_book(self, session: AsyncSession, book_uid: str):
        book_delete = await self.get_book(session, book_uid)

        if book_delete is not None:
            await session.delete(book_delete)
            await session.commit()
            return True
        else:
            return False
