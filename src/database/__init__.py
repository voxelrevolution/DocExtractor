"""src/database/__init__.py
Database connection and ORM setup.

Note: The runtime uses a lightweight sqlite3 store for E02 persistence.
SQLAlchemy remains available for future expansion.
"""

import logging

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


def init_database(database_url: str) -> Session:
    """
    Initialize database connection and create tables.

    Args:
        database_url: PostgreSQL connection string

    Returns:
        SQLAlchemy Session factory
    """
    try:
        engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Database initialized successfully")
        return SessionLocal
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


class Document(Base):
    """Minimal Document ORM model.

    This exists to keep SQLAlchemy imports safe and to enable future ORM-backed
    persistence work without breaking module import.
    """

    __tablename__ = "documents"

    document_id = Column(String, primary_key=True)
    sha256 = Column(String, unique=True, nullable=False)
    filename = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    created_at = Column(String, nullable=False)
