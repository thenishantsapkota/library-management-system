from datetime import datetime, timedelta

from api.config import api_config
from api.core.auth.models import User_Pydantic, UserModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

    @classmethod
    def verify_password(cls, password: str, hash: str):
        return cls.pwd_context.verify(password, hash)

    @classmethod
    def hash_password(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    async def authenticate_user(cls, username: str, password: str):
        user = await UserModel.get_or_none(username=username)
        if not user:
            return False
        if not cls.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=api_config.access_token_expire)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, api_config.secret_key, algorithm=api_config.algorithm
        )

        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token, api_config.secret_key, algorithms=[api_config.algorithm]
            )
            user = await UserModel.get(id=payload.get("id"))
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization token",
            )

        return await User_Pydantic.from_tortoise_orm(user)


class SuperUserValidator:
    def __call__(self, user: User_Pydantic = Depends(AuthService.get_current_user)):
        if not user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail="You are not permitted to perform this operation",
            )
