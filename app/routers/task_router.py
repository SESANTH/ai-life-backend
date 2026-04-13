from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Task
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdateStatus
from datetime import datetime, timedelta, date


router = APIRouter()

# CREATE TASK
@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
    title=task.title,
    date=datetime.strptime(task.date, "%Y-%m-%d").date()
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# GET TASKS
@router.get("/tasks/today", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

from fastapi import HTTPException

# UPDATE TASK STATUS
@router.put("/tasks/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, update: TaskUpdateStatus, db: Session = Depends(get_db)):
    
    task = db.query(Task).filter(Task.id == task_id).first()

    task.status = update.status.lower()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # CORE LOGIC
    if update.status == "missed":
        current_date = task.date
        new_date = current_date + timedelta(days=1)

        task.date = new_date

        task.date = new_date.strftime("%Y-%m-%d")
        task.status = "pending"

    else:
        task.status = update.status

    db.commit()
    db.refresh(task)

    return task

@router.get("/suggestions")
def get_suggestions(db: Session = Depends(get_db)):

    today = date.today()
    yesterday = today - timedelta(days=1)

    tasks = db.query(Task).all()

    suggestions = []

    for task in tasks:
        if task.status == "missed" and task.date == yesterday:

            suggestions.append({
                "message": f"You missed {task.title} yesterday. Let’s complete it today 💪",
                "task": task.title
            })

    return {"suggestions": suggestions}


@router.get("/streaks")
def get_streaks(db: Session = Depends(get_db)):

    tasks = db.query(Task).all()

    streak_data = {}

    for task in tasks:
        if task.status == "done":
            streak_data[task.title] = streak_data.get(task.title, 0) + 1

    return {"streaks": streak_data}


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    today = date.today()
    yesterday = today - timedelta(days=1)

    tasks = db.query(Task).all()

    today_tasks = []
    suggestions = []
    streaks = {}

    for task in tasks:

        #  Today tasks
        if task.date == today:
            today_tasks.append({
                "id": task.id,
                "title": task.title,
                "status": task.status
            })

        #  Suggestions (missed yesterday)
        if task.status == "missed" and task.date == yesterday:
            suggestions.append({
                "message": f"You missed {task.title} yesterday. Let’s complete it today 💪",
                "task": task.title
            })

        #  Streak logic
        if task.status == "done":
            streaks[task.title] = streaks.get(task.title, 0) + 1

    return {
        "today_tasks": today_tasks,
        "suggestions": suggestions,
        "streaks": streaks
    }
