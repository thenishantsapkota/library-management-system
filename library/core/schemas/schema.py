from lib2to3.pytree import Base
from pydantic import BaseModel


class BooksSchema(BaseModel):
    name: str
    description: str
    category: str
    author: str
    publisher: str
    price: float
    code: str
