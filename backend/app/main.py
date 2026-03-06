from fastapi import FastAPI
from app.routes import auth
from app.database import Base, engine
from app.routes import resume 
from app.routes import roadmap
from app.models.course import Course


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(resume.router) 
app.include_router(roadmap.router)