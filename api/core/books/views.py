from api.core.auth.models import User_Pydantic
from api.core.auth.service import AuthService, SuperUserValidator
from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from .models import Book_Pydantic, BookIn_Pydantic, BookModel, BookOut_Pydantic

router = InferringRouter(tags=["Books"])
validate_superuser = SuperUserValidator()


@cbv(router)
class BookView:
    auth_service = AuthService

    @router.get("/")
    async def get_all_books(
        self, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        data = await Book_Pydantic.from_queryset(BookModel.all())
        if not data:
            raise HTTPException(status_code=404, detail="No books could be found!")
        return {
            "success": True,
            "data": data,
            "message": "All books fetched successfully!",
        }

    @router.get("/{book_id}")
    async def get_one_book(
        self, book_id: int, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        book_obj = await BookModel.get_or_none(id=book_id)
        if not book_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book not found for Id {book_id}",
            )
        data = await BookOut_Pydantic.from_tortoise_orm(book_obj)
        return {
            "success": True,
            "data": data,
            "message": "Book retrieved successfully!",
        }

    @router.post("/add-book", dependencies=[Depends(validate_superuser)])
    async def add_book(
        self,
        book: BookIn_Pydantic,
        _: User_Pydantic = Depends(auth_service.get_current_user),
    ):
        book_obj = await BookModel.create(**book.dict(exclude_unset=True))
        data = await BookOut_Pydantic.from_tortoise_orm(book_obj)
        return {"success": True, "data": data, "message": "Book added successfully!"}

    @router.put("/update-book/{book_id}", dependencies=[Depends(validate_superuser)])
    async def update_book(
        self,
        book_id: int,
        book: BookIn_Pydantic,
        _: User_Pydantic = Depends(auth_service.get_current_user),
    ):
        query = await BookModel.filter(id=book_id).update(
            **book.dict(exclude_unset=True)
        )
        if not query:
            raise HTTPException(
                status_code=404, detail=f"Book not found for Id {book_id}"
            )
        data = await BookOut_Pydantic.from_queryset_single(BookModel.get(id=book_id))
        return {"success": True, "data": data, "message": "Book updated successfully!"}

    @router.delete("/delete-book/{book_id}", dependencies=[Depends(validate_superuser)])
    async def delete_book(
        self, book_id: int, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        model = await BookModel.get_or_none(id=book_id)

        if not model:
            raise HTTPException(
                status_code=404, detail=f"Book not found for Id {book_id}"
            )
        data = await BookOut_Pydantic.from_tortoise_orm(model)
        await model.delete()
        return {"success": True, "data": data, "message": "Book deleted successfully!"}
