from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    model_version = Column(String)
    result = Column(String)
    tampering = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)
