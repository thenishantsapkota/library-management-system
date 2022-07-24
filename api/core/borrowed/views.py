from api.core.auth.models import User_Pydantic
from api.core.auth.service import AuthService, SuperUserValidator
from api.core.borrowed.models import BookBorrowed_Pydantic, BorrowModel
from api.core.paginations import paginate
from api.utils import CustomResponse as cr
from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import IntegrityError

router = InferringRouter(tags=["Borrowed"])
validate_superuser = SuperUserValidator()


@cbv(router)
class BorrowedView:
    auth_service = AuthService

    @router.get("/", dependencies=[Depends(validate_superuser)])
    async def get_all_borrows(
        self,
        page_num: int = 1,
        page_size: int = 5,
        _: User_Pydantic = Depends(auth_service.get_current_user),
    ):
        data = await BookBorrowed_Pydantic.from_queryset(BorrowModel.all())
        if not data:
            paginated_response = []
        paginated_response = paginate(
            base_url="borrowed", data=data, page_num=page_num, page_size=page_size
        )
        return cr.success(paginated_response, "All book borrows fetched successfully!")

    @router.get("/{borrow_id}", dependencies=[Depends(validate_superuser)])
    async def get_one_borrow(
        self, borrow_id: int, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        borrowed_obj = await BorrowModel.get_or_none(id=borrow_id)
        if not borrowed_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No borrow with ID '{borrow_id}' could be found",
            )
        data = await BookBorrowed_Pydantic.from_tortoise_orm(borrowed_obj)
        return cr.success(data, message="Borrow fetched successfully!")

    @router.post("/borrow-book", dependencies=[Depends(validate_superuser)])
    async def borrow_book(
        self,
        borrow: BookBorrowed_Pydantic,
        _: User_Pydantic = Depends(auth_service.get_current_user),
    ):
        try:
            borrowed_obj = await BorrowModel.create(**borrow.dict(exclude_unset=True))
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is already borrowed.",
            )

        data = await BookBorrowed_Pydantic.from_tortoise_orm(borrowed_obj)
        return cr.success(data=data, message="Book borrowed successfully.")
