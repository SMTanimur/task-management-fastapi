from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from .base import TimestampModel

if TYPE_CHECKING:
    from .user import User

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(TimestampModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    
    # Foreign keys
    creator_id: Optional[int] = Field(default=None, foreign_key="users.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationships
    creator: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Task.creator_id==User.id",
            "back_populates": "tasks_created"
        }
    )
    assignee: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Task.assignee_id==User.id",
            "back_populates": "tasks_assigned"
        }
    ) 