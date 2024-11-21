from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import UserService
from schemas import user_schema
from utils.token_util import create_access_token, verify_token
from datetime import timedelta
from typing import Annotated, List

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = UserService.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=user_schema.UserResponse)
async def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)

@router.post("/login", response_model=user_schema.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=user_schema.UserResponse)
async def read_users_me(
    current_user: Annotated[user_schema.UserResponse, Depends(get_current_user)]
):
    return current_user

@router.get("", response_model=List[user_schema.UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Annotated[user_schema.UserResponse, Depends(get_current_user)]
):
    return UserService.get_all_users(db, skip=skip, limit=limit)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[user_schema.UserResponse, Depends(get_current_user)]
):
    return UserService.delete_user(db, user_id)

@router.post("/{user_id}/restore")
async def restore_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[user_schema.UserResponse, Depends(get_current_user)]
):
    return UserService.restore_user(db, user_id)
