from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session
from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book API",
    description="A simple REST API for managing a collection of books",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

class BookBase(BaseModel):
    title: str = Field(..., description="The title of the book", example="The Great Gatsby")
    author: str = Field(..., description="The author of the book", example="F. Scott Fitzgerald")

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int = Field(..., description="The unique identifier for the book")

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    message: str = Field(..., description="Error message")
    code: int = Field(..., description="HTTP status code")

@app.get(
    "/books",
    response_model=List[Book],
    summary="Get all books",
    description="Retrieve a list of all books in the collection",
    response_description="List of books"
)
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.BookDB).all()

@app.get(
    "/books/{book_id}",
    response_model=Book,
    summary="Get a book by ID",
    description="Retrieve a specific book by its ID",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"},
        400: {"model": ErrorResponse, "description": "Invalid book ID"}
    }
)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookDB).filter(models.BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a new book to the collection",
    responses={
        201: {"description": "Book successfully created"},
        400: {"model": ErrorResponse, "description": "Invalid input"}
    }
)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    if not book.title or not book.author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and author are required"
        )
    db_book = models.BookDB(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put(
    "/books/{book_id}",
    response_model=Book,
    summary="Update a book",
    description="Update an existing book's information",
    responses={
        200: {"description": "Book successfully updated"},
        404: {"model": ErrorResponse, "description": "Book not found"},
        400: {"model": ErrorResponse, "description": "Invalid input"}
    }
)
async def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    if not updated_book.title or not updated_book.author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title and author are required"
        )
    db_book = db.query(models.BookDB).filter(models.BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    for key, value in updated_book.model_dump().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Remove a book from the collection",
    responses={
        204: {"description": "Book successfully deleted"},
        404: {"model": ErrorResponse, "description": "Book not found"}
    }
)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.BookDB).filter(models.BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    db.delete(db_book)
    db.commit()
    return None

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) 