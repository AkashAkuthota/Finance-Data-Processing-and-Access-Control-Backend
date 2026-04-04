from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard_service import (
    get_summary,
    get_category_breakdown,
    get_recent_transactions,
    get_monthly_trends
)
from app.core.dependencies import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(require_role(["viewer", "analyst", "admin"]))):
    return get_summary(db)


@router.get("/category")
def category(db: Session = Depends(get_db), user=Depends(require_role(["viewer", "analyst", "admin"]))):
    return get_category_breakdown(db)


@router.get("/recent")
def recent(db: Session = Depends(get_db), user=Depends(require_role(["viewer", "analyst", "admin"]))):
    return get_recent_transactions(db)


@router.get("/trends")
def trends(db: Session = Depends(get_db), user=Depends(require_role(["viewer", "analyst", "admin"]))):
    return get_monthly_trends(db)

