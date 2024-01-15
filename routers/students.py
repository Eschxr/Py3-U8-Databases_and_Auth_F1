from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models import Students
from database import get_db
from .auth import get_current_user

router = APIRouter()


class Student(BaseModel):
    id: int | None = None
    name: str = Field(min_length=3)
    gender: str = Field(min_length=4)
    grad_year: str = Field(min_length=4)
    gpa: str = Field(min_length=2)
    fav_class: str = Field(min_length=3)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "name of student",
                "gender": "gender of the student",
                "grad_year": "year the student will graduate",
                "gpa": "3.0",
                "fav_class": "student's favorite class"
            }
        }


@router.get("", status_code=status.HTTP_200_OK)
async def get_student_registry(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user:
        return db.query(Students).all()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: Student, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_task = Students(**student_data.model_dump())

    db.add(new_task)
    db.commit()

# @router.post("", status_code=status.HTTP_201_CREATED)
# async def create_student(student_data: Student, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
#     if "admin" in current_user.get("role"):
#         new_student = Students(**student_data.model_dump())

#         db.add(new_student)
#         db.commit()
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.get("/{student_id}", status_code=status.HTTP_200_OK)
async def get_student_by_id(student_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user:
        student = db.query(Students).filter(student_id == Students.id).first()
        if student is not None:
            return student

        raise HTTPException(status_code=404, detail=f"Student with id#{student_id} not found")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.put("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student_by_id(student_id: int, student_data: Student, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    student = db.query(Students).filter(student_id == Students.id).first()

    if student is None:
        raise HTTPException(status_code=404, detail=f"Student with id#{student_id} not found")

    student.name = student_data.name
    student.gender = student_data.gender
    student.grad_year = student_data.grad_year
    student.gpa = student_data.gpa
    student.fav_class = student_data.fav_class

    db.add(student)
    db.commit()


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_by_id(student_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    delete_student = db.query(Students).filter(Students.id == student_id).first()

    if delete_student is None:
        raise HTTPException(status_code=404, detail=f"Student with id#{student_id} not found")

    db.query(Students).filter(Students.id == student_id).delete()
    db.commit()