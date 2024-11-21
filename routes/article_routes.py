from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.article_service import ArticleService
from schemas import user_data_schema
from routes.user_routes import get_current_user
from schemas.user_schema import UserResponse
from typing import List, Annotated

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=user_data_schema.UserDataResponse)
async def create_article(
    article: user_data_schema.UserDataCreate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return ArticleService.create_article(db, article, current_user.id)

@router.get("/", response_model=List[user_data_schema.UserDataResponse])
async def get_user_articles(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return ArticleService.get_user_articles(db, current_user.id)

@router.get("/{article_id}", response_model=user_data_schema.UserDataResponse)
async def get_article(
    article_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    article = ArticleService.get_article(db, article_id)
    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this article"
        )
    return article

@router.put("/{article_id}", response_model=user_data_schema.UserDataResponse)
async def update_article(
    article_id: int,
    article_update: user_data_schema.UserDataUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return ArticleService.update_article(db, article_id, article_update, current_user.id)

@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return ArticleService.delete_article(db, article_id, current_user.id)
