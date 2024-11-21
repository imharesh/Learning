from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user_data_model import UserData
from schemas import user_data_schema
from typing import List

class ArticleService:
    @staticmethod
    def create_article(db: Session, article: user_data_schema.UserDataCreate, user_id: int):
        db_article = UserData(
            **article.dict(),
            user_id=user_id
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def get_article(db: Session, article_id: int):
        article = db.query(UserData).filter(UserData.id == article_id).first()
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        return article

    @staticmethod
    def get_user_articles(db: Session, user_id: int) -> List[UserData]:
        return db.query(UserData).filter(UserData.user_id == user_id).all()

    @staticmethod
    def update_article(db: Session, article_id: int, article_update: user_data_schema.UserDataUpdate, user_id: int):
        db_article = db.query(UserData).filter(
            UserData.id == article_id,
            UserData.user_id == user_id
        ).first()
        
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found or you don't have permission to modify it"
            )

        update_data = article_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_article, field, value)

        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def delete_article(db: Session, article_id: int, user_id: int):
        db_article = db.query(UserData).filter(
            UserData.id == article_id,
            UserData.user_id == user_id
        ).first()
        
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found or you don't have permission to delete it"
            )

        db.delete(db_article)
        db.commit()
        return {"message": "Article deleted successfully"}
