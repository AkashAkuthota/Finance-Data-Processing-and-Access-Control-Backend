from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True)

    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income / expense
    category = Column(String, nullable=False)

    date = Column(Date, nullable=False)
    description = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="records")