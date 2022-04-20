from fastapi import FastAPI
from tortoise import Tortoise

from api.core.books.views import router as books
from api.core.tortoise_config import tortoise_config

app = FastAPI(
    title="Library Management System - Backend",
    docs_url="/",
    redoc_url=None,
    version="0.1.0",
)

app.include_router(books, prefix="/api/v1/books")


@app.on_event("startup")
async def on_startup():
    await Tortoise.init(tortoise_config)
