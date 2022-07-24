import logging

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from tortoise import Tortoise

from api.core.auth.views import router as auth
from api.core.books.views import router as books
from api.core.borrowed.views import router as borrowed
from api.core.students.views import router as students
from api.core.tortoise_config import tortoise_config

from . import __version__

logger = logging.getLogger("main")

tags = [
    {
        "name": "Authentication",
        "description": "All the operations related to user authentication",
    },
    {"name": "Books", "description": "All the operations related to books"},
    {
        "name": "Students",
        "description": "All the operations related to Student management",
    },
    {"name": "Borrowed", "description": "All the operations related to Book Borrowing"},
]

app = FastAPI(
    title="Library Management System - Backend",
    docs_url="/",
    redoc_url=None,
    version=__version__,
    contact={
        "name": "Nishant Sapkota",
        "url": "https://thenishantsapkota.github.io",
        "email": "snishant306@gmail.com",
    },
    openapi_tags=tags,
)


app.include_router(auth, prefix="/api/auth")
app.include_router(books, prefix="/api/books")
app.include_router(students, prefix="/api/students")
app.include_router(borrowed, prefix="/api/borrowed")


@app.on_event("startup")
async def on_startup():
    await Tortoise.init(tortoise_config)
    logger.debug("Connected to Database!")


@app.exception_handler(Exception)
async def handle_exceptions(_, err: Exception):
    return JSONResponse(
        content={"success": False, "message": str(err)}, status_code=400
    )


@app.exception_handler(HTTPException)
async def handle_http_exception(_, err: HTTPException):
    return JSONResponse(
        content={"success": False, "message": err.detail}, status_code=err.status_code
    )


if __name__ == "__main__":
    uvicorn.run(app)
