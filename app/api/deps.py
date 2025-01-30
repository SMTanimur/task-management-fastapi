from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.models.user import User

def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    # Get token from cookie
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise credentials_exception
        
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 