from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(Date)
    status = Column(String)

    # ADD THIS LINE
    user_id = Column(Integer, ForeignKey("users.id"))