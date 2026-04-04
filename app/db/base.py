# Base class for all SQLAlchemy models
# All ORM models will inherit from this class
# This enables SQLAlchemy to track and map database tables properly

from sqlalchemy.orm import declarative_base

Base = declarative_base()
