from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


def get_or_404(db: Session, model, obj_id: int):
    obj = db.get(model, obj_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@router.get("/courses", response_model=list[schemas.CourseOut])
def list_courses(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Course)
    if search:
        query = query.filter(models.Course.title.ilike(f"%{search}%"))
    if category_id is not None:
        query = query.filter(models.Course.category_id == category_id)
    if teacher_id is not None:
        query = query.filter(models.Course.teacher_id == teacher_id)
    return query.all()


@router.post(
    "/courses",
    response_model=schemas.CourseOut,
    status_code=status.HTTP_201_CREATED,
)
def create_course(payload: schemas.CourseCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.User, payload.teacher_id)
    get_or_404(db, models.Category, payload.category_id)
    course = models.Course(
        title=payload.title,
        description=payload.description,
        teacher_id=payload.teacher_id,
        category_id=payload.category_id,
        created_at=now_iso(),
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(
    course_id: int,
    payload: schemas.CourseUpdate,
    db: Session = Depends(get_db),
):
    course = get_or_404(db, models.Course, course_id)
    data = payload.model_dump(exclude_unset=True)
    if "teacher_id" in data:
        get_or_404(db, models.User, data["teacher_id"])
    if "category_id" in data:
        get_or_404(db, models.Category, data["category_id"])
    for key, value in data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = get_or_404(db, models.Course, course_id)
    db.delete(course)
    db.commit()
    return None


@router.get("/lessons", response_model=list[schemas.LessonOut])
def list_lessons(
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Lesson)
    if course_id is not None:
        query = query.filter(models.Lesson.course_id == course_id)
    return query.all()


@router.post(
    "/enrollments",
    response_model=schemas.EnrollmentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_enrollment(payload: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.User, payload.user_id)
    get_or_404(db, models.Course, payload.course_id)
    existing = (
        db.query(models.Enrollment)
        .filter_by(user_id=payload.user_id, course_id=payload.course_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already enrolled in this course",
        )
    enrollment = models.Enrollment(
        user_id=payload.user_id,
        course_id=payload.course_id,
        enrolled_at=now_iso(),
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.post(
    "/submissions",
    response_model=schemas.SubmissionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_submission(payload: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    get_or_404(db, models.Assignment, payload.assignment_id)
    get_or_404(db, models.User, payload.user_id)
    submission = models.Submission(
        assignment_id=payload.assignment_id,
        user_id=payload.user_id,
        content=payload.content,
        score=None,
        status="pending",
        submitted_at=now_iso(),
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.put("/submissions/{submission_id}", response_model=schemas.SubmissionOut)
def update_submission(
    submission_id: int,
    payload: schemas.SubmissionUpdate,
    db: Session = Depends(get_db),
):
    submission = get_or_404(db, models.Submission, submission_id)
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(submission, key, value)
    db.commit()
    db.refresh(submission)
    return submission
