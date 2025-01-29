from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.task import TaskPriority, TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO

class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    assignee_id: Optional[int] = None

class TaskInDBBase(TaskBase):
    id: int
    creator_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Task(TaskInDBBase):
    pass 