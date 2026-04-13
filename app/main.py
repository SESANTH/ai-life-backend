from fastapi import FastAPI
from app.db.database import engine, Base
from app.db import models
from app.routers import task_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#create tables
Base.metadata.create_all(bind=engine)

app.include_router(task_router.router)

@app.get("/")
def root():
    return {"message": "AI Life Assistant Backend Running 🚀"}

from app.routers import chat_router

app.include_router(chat_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)