from app.database import SessionLocal
from app.models.job import Job

db = SessionLocal()

jobs = [
    {
        "title": "Frontend Developer",
        "company": "TechCorp",
        "location": "Bangalore",
        "salary": "6 LPA",
        "required_skills": "React,JavaScript,HTML,CSS",
        "link": "https://example.com/job1"
    },
    {
        "title": "React Developer",
        "company": "StartupX",
        "location": "Remote",
        "salary": "7 LPA",
        "required_skills": "React,JavaScript",
        "link": "https://example.com/job2"
    },
    {
        "title": "Full Stack Developer",
        "company": "DevWorks",
        "location": "Chennai",
        "salary": "8 LPA",
        "required_skills": "React,Node.js,MongoDB",
        "link": "https://example.com/job3"
    }
]

for j in jobs:
    job = Job(**j)
    db.add(job)

db.commit()
db.close()

print("Jobs seeded successfully")