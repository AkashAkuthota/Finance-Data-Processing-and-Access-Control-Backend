from fastapi import FastAPI
from sqlalchemy.orm import Session
import logging

from app.db.base import Base
from app.db.session import engine, SessionLocal

# Register models
from app.models import user, role, financial_record, refresh_token

# Routes
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.finance_routes import router as finance_router
from app.routes.dashboard_routes import router as dashboard_router

from app.models.role import Role

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Finance Backend System",
    description="A comprehensive finance dashboard backend with role-based access control",
    version="1.0.0"
)


# Create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")


# 🔥 ROLE SEEDING
def seed_roles():
    db: Session = SessionLocal()

    roles = ["viewer", "analyst", "admin"]

    for r in roles:
        exists = db.query(Role).filter(Role.name == r).first()
        if not exists:
            db.add(Role(name=r))
            logger.info(f"Created role: {r}")

    db.commit()
    db.close()
    logger.info("Role seeding completed")


seed_roles()


# Register routes
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(finance_router)
app.include_router(dashboard_router)

logger.info("All routes registered successfully")
logger.info("Finance Backend System started")