from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .user_model import Base

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(Text)
    title = Column(String, nullable=False)
    user_input = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Foreign key relationship with User
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="articles")

    def __repr__(self):
        return f"<UserData {self.title}>"
