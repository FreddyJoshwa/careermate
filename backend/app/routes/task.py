from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.services.validation_service import submit_and_validate_task
from app.models.task import Task

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks")
def get_tasks(credentials=Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "week": t.week,
                "task_title": t.task_title,
                "task_description": t.task_description,
                "skill": t.skill,
                "status": t.status
            }
            for t in tasks
        ]
    }

@router.post("/tasks/submit")
def submit_task(data: dict, credentials=Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    result = submit_and_validate_task(
        db=db,
        user_id=user_id,
        task_id=data.get("task_id"),
        submission_text=data.get("submission_text"),
        github_link=data.get("github_link")
    )

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return result