from pydantic import BaseModel, Field, validator
from datetime import date as Date
from typing import Optional, Literal


class RecordCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")
    type: Literal["income", "expense"] = Field(..., description="Transaction type")
    category: str = Field(..., min_length=1, max_length=50, description="Transaction category")
    date: Date = Field(..., description="Transaction date")
    description: Optional[str] = Field(None, max_length=200, description="Optional transaction description")

    @validator('category')
    def validate_category(cls, v):
        return v.strip().lower()


class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[Date] = None
    description: Optional[str] = Field(None, max_length=200)

    @validator('category')
    def validate_category(cls, v):
        return v.strip().lower() if v else v