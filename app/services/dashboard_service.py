from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.financial_record import FinancialRecord
import logging

logger = logging.getLogger(__name__)


def get_summary(db: Session):
    income = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == "income",
        FinancialRecord.is_deleted == False
    ).scalar() or 0

    expense = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.type == "expense",
        FinancialRecord.is_deleted == False
    ).scalar() or 0

    logger.info(f"Dashboard summary: income={income}, expense={expense}, balance={income-expense}")
    return {
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    }


def get_category_breakdown(db: Session):
    result = db.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount)
    ).filter(
        FinancialRecord.is_deleted == False
    ).group_by(FinancialRecord.category).all()

    breakdown = [{"category": r[0], "total": r[1]} for r in result]
    logger.info(f"Category breakdown generated with {len(breakdown)} categories")
    return breakdown


def get_recent_transactions(db: Session, limit: int = 5):
    records = db.query(FinancialRecord)\
        .filter(FinancialRecord.is_deleted == False)\
        .order_by(FinancialRecord.date.desc())\
        .limit(limit)\
        .all()

    logger.info(f"Retrieved {len(records)} recent transactions")
    return records


def get_monthly_trends(db: Session):
    result = db.query(
        func.date_trunc('month', FinancialRecord.date),
        func.sum(FinancialRecord.amount)
    ).filter(
        FinancialRecord.is_deleted == False
    ).group_by(
        func.date_trunc('month', FinancialRecord.date)
    ).order_by(
        func.date_trunc('month', FinancialRecord.date)
    ).all()

    trends = [{"month": str(r[0]), "total": r[1]} for r in result]
    logger.info(f"Monthly trends generated for {len(trends)} months")
    return trends