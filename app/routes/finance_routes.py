from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import logging

from app.core.dependencies import require_role
from app.db.session import get_db
from app.schemas.financial_record import RecordCreate, RecordUpdate
from app.services.finance_service import (
    create_record,
    get_records,
    update_record,
    delete_record,
    search_records
)
from app.utils.rate_limiter import rate_limit

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/records", tags=["Finance"])


@router.post("/")
def create(
    record: RecordCreate,
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    try:
        key = f"create_record:{user.id}"
        rate_limit(key, limit=10, window=60)  # 10 records per minute per user

        logger.info(f"User {user.email} creating financial record: {record.amount} {record.type}")
        result = create_record(db, user.id, record.dict())
        logger.info(f"Record created with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating record for user {user.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/")
def read(
    page: int = 1,
    limit: int = 10,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    user=Depends(require_role(["analyst", "admin"]))
):
    filters = {
        "type": type,
        "category": category,
        "start_date": start_date,
        "end_date": end_date
    }

    logger.info(f"User {user.email} fetching records with filters: {filters}, page: {page}, limit: {limit}")
    return get_records(db, filters, page, limit)


@router.put("/{record_id}")
def update(
    record_id: int,
    data: RecordUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    logger.info(f"User {user.email} updating record {record_id} with data: {data.dict(exclude_unset=True)}")
    updated = update_record(db, record_id, data.dict(exclude_unset=True))

    if not updated:
        logger.warning(f"Record {record_id} not found for update by user {user.email}")
        raise HTTPException(status_code=404, detail="Record not found")

    logger.info(f"Record {record_id} updated successfully")
    return updated


@router.get("/search")
def search(
    q: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(require_role(["analyst", "admin"]))
):
    logger.info(f"User {user.email} searching for: '{q}', page: {page}, limit: {limit}")
    return search_records(db, q, page, limit)