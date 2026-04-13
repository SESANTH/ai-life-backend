from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.ai_service import parse_user_input
from app.db.models import Task

import json

router = APIRouter()


@router.post("/chat")
def chat(user_input: str, db: Session = Depends(get_db)):

    ai_response = parse_user_input(user_input)

    try:
        parsed = json.loads(ai_response)
    except:
        return {"error": "AI response parsing failed", "raw": ai_response}

    print("AI PARSED:", parsed)

    #  Ensure always list (multi-action support)
    if isinstance(parsed, dict):
        parsed = [parsed]

    results = []

    tasks = db.query(Task).all()

    #  LOOP through each action
    for item in parsed:

        action = item.get("action")
        task_name = item.get("task")

        if not task_name:
            results.append({"task": None, "status": "invalid input"})
            continue

        matched_task = None

        #  Exact match
        for t in tasks:
            if task_name.lower() in t.title.lower():
                matched_task = t
                break

        #  Partial match fallback
        if not matched_task:
            for t in tasks:
                if any(word in t.title.lower() for word in task_name.lower().split()):
                    matched_task = t
                    break

        if not matched_task:
            results.append({"task": task_name, "status": "not found"})
            continue

        print("MATCHED TASK:", matched_task.title)

        #  Update status
        if action == "mark_done":
            matched_task.status = "done"

        elif action == "mark_missed":
            matched_task.status = "missed"

        results.append({
            "task": matched_task.title,
            "status": matched_task.status
        })

    db.commit()

    return {
        "message": "Multi-action processed",
        "results": results
    }