import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base

class JobStatus(str, enum.Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ItemStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class CertificateJob(Base):
    __tablename__ = "certificate_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(JobStatus), default=JobStatus.COMPLETED)
    total_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("CertificateItem", back_populates="job", cascade="all, delete-orphan")

class CertificateItem(Base):
    __tablename__ = "certificate_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), ForeignKey("certificate_jobs.id"))
    recipient_name = Column(String(255), nullable=False)
    recipient_email = Column(String(255), nullable=False)
    course_name = Column(String(255), nullable=False)
    issue_date = Column(String(50), nullable=False)
    status = Column(Enum(ItemStatus))
    file_path = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)

    job = relationship("CertificateJob", back_populates="items")