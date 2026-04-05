from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        return None
    
    if not user.is_active:
        return None

    access_token = create_access_token({"sub": user.email})
    refresh_token_value = create_refresh_token()

    refresh = RefreshToken(
        token=refresh_token_value,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(refresh)
    db.commit()

    return access_token, refresh_token_value


# ROTATION + REUSE DETECTION
def refresh_tokens(db: Session, token_value: str):
    token = db.query(RefreshToken).filter(RefreshToken.token == token_value).first()

    if not token:
        return None

    #  REUSE DETECTED
    if token.is_revoked:
        # revoke all sessions
        db.query(RefreshToken).filter(
            RefreshToken.user_id == token.user_id
        ).update({"is_revoked": True})

        db.commit()
        return None

    if token.expires_at < datetime.utcnow():
        return None

    # rotate
    token.is_revoked = True

    new_token_value = create_refresh_token()

    new_token = RefreshToken(
        token=new_token_value,
        user_id=token.user_id,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.add(new_token)
    db.commit()

    user = token.user
    access = create_access_token({"sub": user.email})

    return access, new_token_value


def revoke_refresh_token(db: Session, token_value: str):
    token = db.query(RefreshToken).filter(RefreshToken.token == token_value).first()

    if token:
        token.is_revoked = True
        db.commit()