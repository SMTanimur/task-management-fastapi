from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_active_user
from app.core.security import get_password_hash
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()

@router.post("/", response_model=User)
def create_user(
    user_in: UserCreate,
    session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/me", response_model=User)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    if user_in.password:
        current_user.hashed_password = get_password_hash(user_in.password)
    if user_in.email:
        current_user.email = user_in.email
    if user_in.full_name:
        current_user.full_name = user_in.full_name
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

# ... rest of the users endpoints 