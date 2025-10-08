from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
books = [
  {
    "id": 1,
    "title": "The Silent Forest",
    "author": "Amelia Hart",
    "publisher": "Willow Press",
    "published_date": "2018-03-12",
    "page_count": 324,
    "language": "English"
  },
  {
    "id": 2,
    "title": "Echoes of Eternity",
    "author": "Liam Carter",
    "publisher": "Sunrise Publications",
    "published_date": "2020-07-25",
    "page_count": 410,
    "language": "English"
  },
  {
    "id": 3,
    "title": "Beneath the Crimson Sky",
    "author": "Isabella Moore",
    "publisher": "Crescent Books",
    "published_date": "2019-10-05",
    "page_count": 287,
    "language": "English"
  },
  {
    "id": 4,
    "title": "Winds of Tomorrow",
    "author": "Noah Bennett",
    "publisher": "Harbor House",
    "published_date": "2021-01-18",
    "page_count": 350,
    "language": "English"
  },
  {
    "id": 5,
    "title": "The Last Voyage",
    "author": "Sophia Rivera",
    "publisher": "Blue Horizon Press",
    "published_date": "2017-06-02",
    "page_count": 295,
    "language": "English"
  },
  {
    "id": 6,
    "title": "Whispers in the Wind",
    "author": "Ethan Collins",
    "publisher": "Moonlight Books",
    "published_date": "2022-09-14",
    "page_count": 378,
    "language": "English"
  },
  {
    "id": 7,
    "title": "The Forgotten Path",
    "author": "Charlotte Hayes",
    "publisher": "Elmwood Publications",
    "published_date": "2016-11-09",
    "page_count": 312,
    "language": "English"
  },
  {
    "id": 8,
    "title": "Stars Over Avalon",
    "author": "James Turner",
    "publisher": "Aurora House",
    "published_date": "2021-05-27",
    "page_count": 404,
    "language": "English"
  },
  {
    "id": 9,
    "title": "Shadows of the Mind",
    "author": "Emily Brooks",
    "publisher": "Nova Press",
    "published_date": "2019-12-03",
    "page_count": 276,
    "language": "English"
  },
  {
    "id": 10,
    "title": "Journey to the North",
    "author": "Oliver Green",
    "publisher": "Northwind Books",
    "published_date": "2015-04-15",
    "page_count": 338,
    "language": "English"
  },
  {
    "id": 11,
    "title": "The Hidden Garden",
    "author": "Grace Mitchell",
    "publisher": "Evergreen Press",
    "published_date": "2018-09-21",
    "page_count": 250,
    "language": "English"
  },
  {
    "id": 12,
    "title": "A Tale of Two Suns",
    "author": "Benjamin Ross",
    "publisher": "Solaris Publications",
    "published_date": "2023-03-10",
    "page_count": 415,
    "language": "English"
  },
  {
    "id": 13,
    "title": "The Painter’s Secret",
    "author": "Mia Foster",
    "publisher": "Golden Ink",
    "published_date": "2020-02-28",
    "page_count": 289,
    "language": "English"
  },
  {
    "id": 14,
    "title": "Dreams of the Deep",
    "author": "Jacob Allen",
    "publisher": "Coral Press",
    "published_date": "2019-08-16",
    "page_count": 333,
    "language": "English"
  },
  {
    "id": 15,
    "title": "The Iron City",
    "author": "Hannah Lewis",
    "publisher": "Steelworks Publishing",
    "published_date": "2017-12-11",
    "page_count": 360,
    "language": "English"
  },
  {
    "id": 16,
    "title": "Echo Valley",
    "author": "Daniel Young",
    "publisher": "Maple Leaf Books",
    "published_date": "2022-06-08",
    "page_count": 297,
    "language": "English"
  },
  {
    "id": 17,
    "title": "The Secret Compass",
    "author": "Natalie Price",
    "publisher": "Adventure House",
    "published_date": "2018-10-19",
    "page_count": 420,
    "language": "English"
  },
  {
    "id": 18,
    "title": "Beyond the Mountains",
    "author": "Andrew Gray",
    "publisher": "Summit Press",
    "published_date": "2016-02-23",
    "page_count": 318,
    "language": "English"
  },
  {
    "id": 19,
    "title": "The Clockmaker’s Paradox",
    "author": "Ella Ward",
    "publisher": "Timeless Books",
    "published_date": "2021-09-30",
    "page_count": 391,
    "language": "English"
  },
  {
    "id": 20,
    "title": "Whispering Shadows",
    "author": "Ryan Adams",
    "publisher": "Darkwood Publications",
    "published_date": "2020-11-12",
    "page_count": 284,
    "language": "English"
  }
]

class Book(BaseModel):
    id: int
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

@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book)-> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@app.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.patch("/book/{book_id}")
async def update_book(book_id: int, book_update_data:UpdateBook) -> dict:
    
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    