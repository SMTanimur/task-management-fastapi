from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator
from app.models.task import TaskPriority, TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO

    class Config:
        orm_mode = True
        use_enum_values = True

class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None

    @validator('assignee_id')
    def validate_assignee_id(cls, v):
        if v is not None and v <= 0:
            return None
        return v

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    assignee_id: Optional[int] = None

    @validator('assignee_id')
    def validate_assignee_id(cls, v):
        if v is not None and v <= 0:
            return None
        return v

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