from fastapi import FastAPI

from library.core.models import migrate
from library.core.models.database import Books
from library.core.schemas.schema import BooksSchema

app = FastAPI(
    title="Library Management System - Backend",
    docs_url="/",
    redoc_url=None,
    version="0.1.0",
)
MIGRATE= False

if MIGRATE:
    migrate()
