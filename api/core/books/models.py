from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class BookModel(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=200, null=True)
    description = fields.TextField(max_length=200, null=True)
    category = fields.TextField(max_length=200, null=True)
    author = fields.TextField(max_length=200, null=True)
    publisher = fields.TextField(max_length=200, null=True)
    price = fields.FloatField(null=True)
    code = fields.CharField(max_length=200, unique=True, null=True)


Book_Pydantic = pydantic_model_creator(BookModel, name="Book")
BookIn_Pydantic = pydantic_model_creator(
    BookModel, name="BookIn", exclude_readonly=True
)
BookOut_Pydantic = pydantic_model_creator(BookModel, name="BookOut")
