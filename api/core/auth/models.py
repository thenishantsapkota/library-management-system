from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class UserModel(Model):
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(unique=True, max_length=200)
    email = fields.CharField(unique=True, max_length=200)
    full_name = fields.TextField(null=True)
    password = fields.TextField()
    is_superuser = fields.BooleanField(null=True, default=False)


User_Pydantic = pydantic_model_creator(UserModel, name="User")
UserIn_Pydantic = pydantic_model_creator(
    UserModel, name="UserIn", exclude_readonly=True, exclude=("is_superuser",)
)
UserOut_Pydantic = pydantic_model_creator(
    UserModel, name="UserOut", exclude=("password", "is_superuser")
)
