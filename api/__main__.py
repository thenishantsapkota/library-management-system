import logging

import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from api.core.auth.views import router as auth
from api.core.books.views import router as books
from api.core.tortoise_config import tortoise_config

logger = logging.getLogger("main")

tags = [
    {"name": "Books", "description": "All the operations related to books"},
    {
        "name": "Authentication",
        "description": "All the operations related to user authentication",
    },
]

app = FastAPI(
    title="Library Management System - Backend",
    docs_url="/",
    redoc_url=None,
    version="0.1.0",
    contact={
        "name": "Nishant Sapkota",
        "url": "https://thenishantsapkota.github.io",
        "email": "snishant306@gmail.com",
    },
    openapi_tags=tags,
)

app.include_router(books, prefix="/api/v1/books")
app.include_router(auth, prefix="/api/v1/auth")


@app.on_event("startup")
async def on_startup():
    await Tortoise.init(tortoise_config)
    logger.debug("Connected to Database!")


if __name__ == "__main__":
    uvicorn.run(app)
