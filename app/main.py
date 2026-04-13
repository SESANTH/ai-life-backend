from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=False,  # IMPORTANT CHANGE
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.db.database import engine, Base
from app.db import models
from app.routers import task_router, chat_router

Base.metadata.create_all(bind=engine)

app.include_router(task_router.router)
app.include_router(chat_router.router)

@app.get("/")
def root():
    return {"message": "AI Life Assistant Backend Running 🚀"}