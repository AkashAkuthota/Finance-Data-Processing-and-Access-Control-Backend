from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
import logging

from app.db.session import get_db
from app.services.auth_service import login_user, refresh_tokens, revoke_refresh_token
from app.utils.rate_limiter import rate_limit
from app.core.dependencies import security
from app.utils.token_blacklist import blacklist_token
from app.core.config import settings
from app.schemas.auth import LoginRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


# LOGIN
@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    key = f"login:{request.client.host}"
    rate_limit(key)

    logger.info(f"Login attempt for email: {data.email} from IP: {request.client.host}")

    result = login_user(db, data.email, data.password)

    if not result:
        logger.warning(f"Failed login attempt for email: {data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = result

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="strict"
    )

    logger.info(f"Successful login for email: {data.email}")
    return {"access_token": access_token}


# REFRESH
@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    result = refresh_tokens(db, refresh_token)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token, new_refresh_token = result

    # set new cookie (rotation)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="strict"
    )

    return {"access_token": access_token}


# LOGOUT
@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    credentials=Depends(security)
):
    access_token = credentials.credentials

    refresh_token = request.cookies.get("refresh_token")

    # revoke refresh token
    if refresh_token:
        revoke_refresh_token(db, refresh_token)

    # blacklist access token
    blacklist_token(access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    # clear cookie
    response.delete_cookie("refresh_token")

    return {"message": "Logged out successfully"}