from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .base import TimestampModel

if TYPE_CHECKING:
    from .task import Task

class User(TimestampModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # Relationships
    tasks_created: List["Task"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "User.id==Task.creator_id",
            "back_populates": "creator"
        }
    )
    tasks_assigned: List["Task"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "User.id==Task.assignee_id",
            "back_populates": "assignee"
        }
    ) 