from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class BookModel(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=200)
    description = fields.TextField(max_length=200)
    category = fields.TextField(max_length=200)
    author = fields.TextField(max_length=200)
    publisher = fields.TextField(max_length=200)
    price = fields.FloatField()
    code = fields.CharField(max_length=200, unique=True)


Book_Pydantic = pydantic_model_creator(BookModel, name="Book")
BookIn_Pydantic = pydantic_model_creator(
    BookModel, name="BookIn", exclude_readonly=True
)
BookOut_Pydantic = pydantic_model_creator(BookModel, name="BookOut")
