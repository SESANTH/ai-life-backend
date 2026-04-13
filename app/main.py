from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

# Create app FIRST
app = FastAPI()

# CORS (must be immediately after app creation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle preflight (OPTIONS)
@app.options("/{path:path}")
async def options_handler(path: str):
    return Response(status_code=200)

# Import AFTER app creation (important for structure)
from app.db.database import engine, Base
from app.db import models
from app.routers import task_router, chat_router, auth_router

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(task_router.router)
app.include_router(chat_router.router)
app.include_router(auth_router.router)  

#  Root endpoint
@app.get("/")
def root():
    return {"message": "AI Life Assistant Backend Running 🚀"}