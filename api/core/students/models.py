from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class StudentModel(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=200, null=True)
    roll_number = fields.CharField(unique=True, max_length=200)
    date_of_birth = fields.TextField(null=True)
    email = fields.CharField(unique=True, max_length=200)


Student_Pydantic = pydantic_model_creator(StudentModel, name="Student")
StudentIn_Pydantic = pydantic_model_creator(
    StudentModel, exclude_readonly=True, name="StudentIn"
)
