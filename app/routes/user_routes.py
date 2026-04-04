from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate
from app.services.user_service import create_user, update_user_role, set_user_status
from app.core.dependencies import require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created"}


@router.patch("/{user_id}/role")
def change_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    updated = update_user_role(db, user_id, role)

    if not updated:
        raise HTTPException(status_code=404, detail="User/role not found")

    return {"message": "Role updated"}


@router.patch("/{user_id}/status")
def change_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    user=Depends(require_role(["admin"]))
):
    updated = set_user_status(db, user_id, is_active)

    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Status updated"}