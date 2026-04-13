from pydantic import BaseModel
from datetime import date

class TaskCreate(BaseModel):
    title: str
    date: str

class TaskResponse(BaseModel):
    id: int
    title: str
    date: date
    status: str

    class Config:
        from_attributes = True     


class TaskUpdateStatus(BaseModel):
    status: str  # "done" or "missed"