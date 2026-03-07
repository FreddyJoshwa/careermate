from fastapi import FastAPI
from app.database import Base, engine

# Import routes
from app.routes import auth, resume, roadmap, task, project, job, dashboard, interview

# Import models so tables are created
from app.models.course import Course
from app.models.task import Task
from app.models.project import Project
from app.models.task_submission import TaskSubmission
from app.models.job import Job
from app.models.interview_session import InterviewSession

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(task.router)
app.include_router(project.router)
app.include_router(job.router)
app.include_router(dashboard.router)
app.include_router(interview.router)