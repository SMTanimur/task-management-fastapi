from typing import List, Optional
from sqlmodel import Session, select
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_in: TaskCreate, creator: User) -> Task:
        task_data = task_in.dict(exclude_unset=True)
        
        # Remove assignee_id if it's 0 or None
        if not task_data.get('assignee_id'):
            task_data.pop('assignee_id', None)
        else:
            # Verify assignee exists
            assignee = self.session.get(User, task_data['assignee_id'])
            if not assignee:
                raise HTTPException(
                    status_code=400,
                    detail=f"Assignee with id {task_data['assignee_id']} not found"
                )

        task = Task(
            **task_data,
            creator_id=creator.id
        )
        
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def get_user_tasks(self, user_id: int) -> List[Task]:
        statement = select(Task).where(
            (Task.creator_id == user_id) | (Task.assignee_id == user_id)
        )
        return self.session.exec(statement).all()

    def update_task(self, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        task = self.get_task(task_id)
        if not task:
            return None
            
        task_data = task_in.dict(exclude_unset=True)
        for field, value in task_data.items():
            setattr(task, field, value)
            
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
            
        self.session.delete(task)
        self.session.commit()
        return True 