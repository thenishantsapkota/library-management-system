import logging

import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from api.core.books.views import router as books
from api.core.tortoise_config import tortoise_config

logger = logging.getLogger("main")
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
)

app.include_router(books, prefix="/api/v1/books")


@app.on_event("startup")
async def on_startup():
    await Tortoise.init(tortoise_config)
    logger.debug("Connected to Database!")


if __name__ == "__main__":
    uvicorn.run(app)
