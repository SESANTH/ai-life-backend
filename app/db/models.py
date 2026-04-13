from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


# 🔹 USER MODEL (IMPORTANT)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# 🔹 TASK MODEL
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String, default="pending")
    user_id = Column(Integer, ForeignKey("users.id"))