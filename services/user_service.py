from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user_model import User
from schemas import user_schema
from utils.hash_util import get_password_hash, verify_password
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(db: Session, user: user_schema.UserCreate):
        db_user = db.query(User).filter(User.email == user.email, User.is_deleted == False).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            password=hashed_password,
            name=user.name,
            designation=user.designation
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email, User.is_deleted == False).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email, User.is_deleted == False).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Soft delete the user
        user.is_deleted = True
        user.deleted_at = datetime.now()
        db.commit()
        return {"message": "User deleted successfully"}

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).filter(User.is_deleted == False).offset(skip).limit(limit).all()

    @staticmethod
    def restore_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id, User.is_deleted == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deleted user not found"
            )
        
        # Restore the user
        user.is_deleted = False
        user.deleted_at = None
        db.commit()
        return {"message": "User restored successfully"}
