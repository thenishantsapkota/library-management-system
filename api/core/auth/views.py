from api.core.auth.models import (
    User_Pydantic,
    UserIn_Pydantic,
    UserModel,
    UserOut_Pydantic,
)
from api.core.auth.service import AuthService
from api.utils import CustomResponse as cr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import IntegrityError

router = InferringRouter(tags=["Authentication"])


@cbv(router)
class AuthView:
    auth_service = AuthService

    @router.post("/register")
    async def register_user(self, user: UserIn_Pydantic):
        try:
            user_obj = await UserModel.create(
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                password=self.auth_service.hash_password(user.password),
            )
        except IntegrityError:
            raise HTTPException(
                detail="Username or email already exists!", status_code=400
            )
        data = await UserOut_Pydantic.from_tortoise_orm(user_obj)
        return cr.success(data, "User registered successfully!")

    @router.post("/login")
    async def login_user(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = await self.auth_service.authenticate_user(
            form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        user_obj = await User_Pydantic.from_tortoise_orm(user)
        data = user_obj.dict()
        token = self.auth_service.create_access_token(data)

        return cr.success({"access_token": token}, "User logged in successfully!")

    @router.get("/profile")
    async def get_user(
        self, user: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        data = user.dict(exclude={"password", "is_superuser"})
        return cr.success(data, "User fetched successfully!")
