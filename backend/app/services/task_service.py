from app.agents.task_agent import generate_daily_tasks
from app.models.task import Task

def create_tasks_from_roadmap(db, user_id, goal, roadmap, week="week1"):
    if "detailed_roadmap" not in roadmap or week not in roadmap["detailed_roadmap"]:
        return []

    week_data = roadmap["detailed_roadmap"][week]
    generated = generate_daily_tasks(goal, week, week_data)

    created_tasks = []

    for item in generated.get("tasks", []):
        task = Task(
            user_id=user_id,
            week=week,
            task_title=item.get("task_title"),
            task_description=item.get("task_description"),
            skill=item.get("skill"),
            status="pending"
        )
        db.add(task)
        created_tasks.append(task)

    db.commit()

    return [
        {
            "task_title": t.task_title,
            "task_description": t.task_description,
            "skill": t.skill,
            "status": t.status
        }
        for t in created_tasks
    ]