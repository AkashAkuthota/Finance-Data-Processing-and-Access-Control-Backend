from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password


def create_user(db: Session, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None

    role = db.query(Role).filter(Role.name == "viewer").first()

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role_id=role.id
    )

    db.add(user)
    db.commit()

    return user


def update_user_role(db: Session, user_id: int, role_name: str):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.name == role_name).first()

    if not user or not role:
        return None

    user.role_id = role.id
    db.commit()

    return user


def set_user_status(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.is_active = is_active
    db.commit()

    return user