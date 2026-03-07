from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week = Column(String(20), nullable=False)
    task_title = Column(String(255), nullable=False)
    task_description = Column(Text, nullable=True)
    skill = Column(String(100), nullable=True)
    status = Column(String(50), default="pending")