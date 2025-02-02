from fastapi import FastAPI
import uvicorn

import models
from database import engine
from routers import auth, tasks, students

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(students.router, prefix="/students", tags=["students"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
