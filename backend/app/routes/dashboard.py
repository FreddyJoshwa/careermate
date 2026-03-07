from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.models.resume import Resume
from app.models.task import Task
from app.models.task_submission import TaskSubmission
from app.models.project import Project
from app.models.job import Job

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def get_dashboard(credentials=Depends(security), db: Session = Depends(get_db)):

    payload = verify_token(credentials.credentials)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    # Resume
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()

    skills = resume.skills.split(",") if resume and resume.skills else []
    missing_skills = resume.missing_skills.split(",") if resume and resume.missing_skills else []

    # Tasks
    total_tasks = db.query(Task).count()

    completed_tasks = db.query(TaskSubmission).filter(
        TaskSubmission.user_id == user_id,
        TaskSubmission.status == "completed"
    ).count()

    pending_tasks = total_tasks - completed_tasks

    # Projects
    projects = db.query(Project).filter(Project.user_id == user_id).count()

    # Jobs
    jobs = db.query(Job).count()

    # Job readiness calculation
    readiness = 0

    if total_tasks > 0:
        readiness += (completed_tasks / total_tasks) * 40

    if len(skills) > 0:
        readiness += 30

    if projects > 0:
        readiness += 30

    readiness = round(readiness)

    return {

        "skills_summary": {
            "skills_found": len(skills),
            "missing_skills": len(missing_skills)
        },

        "task_summary": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks
        },

        "project_summary": {
            "projects_submitted": projects
        },

        "job_summary": {
            "available_jobs": jobs
        },

        "job_readiness_score": readiness
    }