from email.policy import HTTP

from api.core.auth.models import User_Pydantic
from api.core.auth.service import AuthService, SuperUserValidator
from api.core.students.models import Student_Pydantic, StudentIn_Pydantic, StudentModel
from api.utils import CustomResponse as cr
from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from tortoise.exceptions import IntegrityError

router = InferringRouter(tags=["Students"])
validate_superuser = SuperUserValidator()


@cbv(router)
class StudentView:
    auth_service = AuthService

    @router.get("/", dependencies=[Depends(validate_superuser)])
    async def get_all_students(
        self, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        data = await Student_Pydantic.from_queryset(StudentModel.all())
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No students could be found!",
            )
        return cr.success(data, "All students fetched successfully!")

    @router.get("/{student_id}", dependencies=[Depends(validate_superuser)])
    async def get_one_student(
        self, student_id: int, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        student_obj = await StudentModel.get_or_none(id=student_id)
        if not student_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No student with ID '{student_id}' could be found",
            )
        data = await Student_Pydantic.from_tortoise_orm(student_obj)
        return cr.success(data, "Student fetched successfully!")

    @router.post("/add-student", dependencies=[Depends(validate_superuser)])
    async def add_student(
        self,
        student: StudentIn_Pydantic,
        _: User_Pydantic = Depends(auth_service.get_current_user),
    ):
        try:
            student_obj = await StudentModel.create(**student.dict(exclude_unset=True))
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or roll number already exists!",
            )
        data = await Student_Pydantic.from_tortoise_orm(student_obj)
        return cr.success(data, "Student added successfully!")

    @router.put(
        "/update-student/{student_id}", dependencies=[Depends(validate_superuser)]
    )
    async def update_student(
        self,
        student_id: int,
        student: StudentIn_Pydantic,
        _: User_Pydantic = Depends(auth_service.get_current_user),
    ):
        query = await StudentModel.filter(id=student_id).update(
            **student.dict(exclude_unset=True)
        )
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student not found for ID '{student_id}'",
            )
        data = await Student_Pydantic.from_queryset_single(
            StudentModel.get(id=student_id)
        )
        return cr.success(data, "Student updated successfully!")

    @router.delete(
        "/delete-student/{student_id}", dependencies=[Depends(validate_superuser)]
    )
    async def delete_student(
        self, student_id: int, _: User_Pydantic = Depends(auth_service.get_current_user)
    ):
        model = await StudentModel.get_or_none(id=student_id)
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Student found for id: {student_id}",
            )
        data = await Student_Pydantic.from_tortoise_orm(model)
        await model.delete()
        return cr.success(data, "Student deleted successfully!")
