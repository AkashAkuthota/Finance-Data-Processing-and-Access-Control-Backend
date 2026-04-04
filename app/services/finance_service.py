from sqlalchemy.orm import Session
from app.models.financial_record import FinancialRecord
import logging

logger = logging.getLogger(__name__)


def create_record(db: Session, user_id: int, data: dict):
    record = FinancialRecord(**data, user_id=user_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    logger.info(f"Created financial record ID: {record.id} for user {user_id}")
    return record


def get_records(db: Session, filters: dict, page: int, limit: int):
    query = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)

    # filtering
    if filters.get("type"):
        query = query.filter(FinancialRecord.type == filters["type"])

    if filters.get("category"):
        query = query.filter(FinancialRecord.category == filters["category"])

    if filters.get("start_date"):
        query = query.filter(FinancialRecord.date >= filters["start_date"])

    if filters.get("end_date"):
        query = query.filter(FinancialRecord.date <= filters["end_date"])

    total = query.count()

    offset = (page - 1) * limit
    data = query.offset(offset).limit(limit).all()

    logger.info(f"Retrieved {len(data)} records (total: {total}) with filters: {filters}")
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    }


def update_record(db: Session, record_id: int, data: dict):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()

    if not record:
        logger.warning(f"Record {record_id} not found for update")
        return None

    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    logger.info(f"Updated record {record_id}")
    return record


def delete_record(db: Session, record_id: int):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()

    if not record:
        logger.warning(f"Record {record_id} not found for deletion")
        return False

    record.is_deleted = True
    db.commit()
    logger.info(f"Soft deleted record {record_id}")
    return True


def search_records(db: Session, search_term: str, page: int = 1, limit: int = 10):
    """Search records by description or category"""
    query = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    ).filter(
        (FinancialRecord.description.ilike(f"%{search_term}%")) |
        (FinancialRecord.category.ilike(f"%{search_term}%"))
    )

    total = query.count()
    offset = (page - 1) * limit
    data = query.offset(offset).limit(limit).all()

    logger.info(f"Search for '{search_term}' returned {len(data)} records")
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": data
    }