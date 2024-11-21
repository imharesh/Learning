from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserDataBase(BaseModel):
    title: str
    hashtag: Optional[str] = None
    user_input: str

class UserDataCreate(UserDataBase):
    pass

class UserDataUpdate(UserDataBase):
    title: Optional[str] = None
    user_input: Optional[str] = None

class UserDataResponse(UserDataBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True
