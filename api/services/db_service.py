from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


class DatabaseService:
    """Database service for managing SQLAlchemy engine and session."""

    _instance = None  # Class-level attribute to store the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'engine'):  # Ensure init runs only once
            self.engine = create_engine(settings.DB_CONNECTION, pool_pre_ping=True)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_engine(self):
        """Return the SQLAlchemy engine instance."""
        return self.engine

    def get_session(self):
        """Create a new session."""
        return self.SessionLocal()
