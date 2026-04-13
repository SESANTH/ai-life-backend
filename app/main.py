from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

app = FastAPI()

# ✅ CORS FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FORCE HANDLE OPTIONS (CRITICAL FIX)
@app.options("/{path:path}")
async def options_handler(path: str):
    return Response(status_code=200)

# --- IMPORTS AFTER ---
from app.db.database import engine, Base
from app.db import models
from app.routers import task_router, chat_router

Base.metadata.create_all(bind=engine)

app.include_router(task_router.router)
app.include_router(chat_router.router)

@app.get("/")
def root():
    return {"message": "AI Life Assistant Backend Running 🚀"}