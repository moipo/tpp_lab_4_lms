from typing import Optional

from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):
    title: str
    description: str
    teacher_id: int
    category_id: int


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    teacher_id: Optional[int] = None
    category_id: Optional[int] = None


class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    teacher_id: int
    category_id: int
    created_at: str


class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    title: str
    content: str
    position: int


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    course_id: int
    enrolled_at: str


class SubmissionCreate(BaseModel):
    assignment_id: int
    user_id: int
    content: str


class SubmissionUpdate(BaseModel):
    score: Optional[int] = None
    status: Optional[str] = None


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assignment_id: int
    user_id: int
    content: str
    score: Optional[int] = None
    status: str
    submitted_at: str
