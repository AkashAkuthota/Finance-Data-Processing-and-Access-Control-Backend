from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)

    token = Column(String, unique=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="refresh_tokens")