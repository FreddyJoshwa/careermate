from app.database import SessionLocal
from app.models.course import Course

db = SessionLocal()

sample_courses = [
    {
        "title": "React for Beginners",
        "skill": "React",
        "platform": "Udemy",
        "link": "https://example.com/react-course",
        "price": "499",
        "rating": "4.5",
        "is_sponsored": True
    },
    {
        "title": "Node.js Complete Guide",
        "skill": "Node.js",
        "platform": "Coursera",
        "link": "https://example.com/node-course",
        "price": "Free",
        "rating": "4.6",
        "is_sponsored": False
    },
    {
        "title": "MongoDB Basics",
        "skill": "MongoDB",
        "platform": "YouTube",
        "link": "https://example.com/mongodb-course",
        "price": "Free",
        "rating": "4.4",
        "is_sponsored": False
    },
    {
        "title": "React Crash Course",
        "skill": "React",
        "platform": "YouTube",
        "link": "https://example.com/react-crash",
        "price": "Free",
        "rating": "4.3",
        "is_sponsored": False
    }
]

for item in sample_courses:
    exists = db.query(Course).filter(
        Course.title == item["title"],
        Course.skill == item["skill"]
    ).first()

    if not exists:
        db.add(Course(**item))

db.commit()
db.close()

print("Courses seeded successfully!")