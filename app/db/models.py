from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(Date)   # keep simple for now
    status = Column(String, default="pending")  # pending/done/missed