from datetime import date, datetime
import typing as t

from sqlmodel import Field, SQLModel


class Students(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    name: str
    roll_number: str
    date_of_birth: date
    year: str
    email: str


class Users(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str


class Books(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    category: str = Field(foreign_key="category.name")
    author: str
    publisher: str = Field(foreign_key="publisher.name")
    price: float
    code: str


class Category(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    name: str


class Publisher(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    name: str


class BorrowedBooks(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    book_name: str = Field(default=None, foreign_key="books.name")
    book_code: str = Field(default=None, foreign_key="books.code")
    borrow_date: datetime = Field(default=datetime.utcnow(), nullable=False)
    return_date: datetime
    student_name: str = Field(foreign_key="students.name")
    student_roll: str = Field(foreign_key="students.roll_number")


class ReturnedBooks(SQLModel, table=True):
    id: t.Optional[int] = Field(default=None, primary_key=True)
    book_name: str = Field(default=None, foreign_key="books.name")
    book_code: str = Field(default=None, foreign_key="books.code")
    student_name: str = Field(default=None, foreign_key="students.name")
    student_roll: str = Field(default=None, foreign_key="students.roll_number")
