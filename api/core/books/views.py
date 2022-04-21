from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from .models import Book_Pydantic, BookIn_Pydantic, BookModel

router = InferringRouter(tags=["Books"])


@cbv(router)
class BookView:
    @router.get("/", response_model=Book_Pydantic)
    async def get_all_books(self):
        data = await Book_Pydantic.from_queryset(BookModel.all())
        if not data:
            raise HTTPException(status_code=404, detail="No books could be found!")
        return {"success": True, "data": data}

    @router.post("/add-book")
    async def add_book(self, book: BookIn_Pydantic):
        book_obj = await BookModel.create(**book.dict(exclude_unset=True))
        data = await Book_Pydantic.from_tortoise_orm(book_obj)
        return {"success": True, "data": data}

    @router.put("/update-book/{book_id}")
    async def update_book(self, book_id: int, book: BookIn_Pydantic):
        model = await BookModel.filter(id=book_id).update(
            **book.dict(exclude_unset=True)
        )
        if not model:
            raise HTTPException(
                status_code=404, detail="No Book with the specified Id could be found!"
            )
        data = await Book_Pydantic.from_queryset_single(BookModel.get(id=book_id))
        return {"success": True, "data": data}

    @router.delete("/delete-book/{book_id}")
    async def delete_book(self, book_id: int):
        model = await BookModel.get_or_none(id=book_id)
        if not model:
            raise HTTPException(
                status_code=404, detail="No book with the specified Id could be found!"
            )
        await model.delete()
        return {"success": True, "message": "Book deleted successfully!"}
