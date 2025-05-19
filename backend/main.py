from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks: List[Task] = []
task_id_counter = 1

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/api/tasks", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    task.id = task_id_counter
    tasks.append(task)
    task_id_counter += 1
    return task

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Task deleted"}

