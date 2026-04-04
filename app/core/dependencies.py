from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.config import settings
from app.utils.token_blacklist import is_token_blacklisted

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user


def require_role(roles: list):
    def checker(user=Depends(get_current_user)):
        if user.role.name not in roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker