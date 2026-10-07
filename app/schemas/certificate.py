from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class RecipientData(BaseModel):
    recipient_name: str = Field(..., min_length=2, max_length=250)
    recipient_email: EmailStr
    course_name: str = Field(..., min_length=2, max_length=250)
    issue_date: str

class BulkCertificateRequest(BaseModel):
    recipients: List[RecipientData]

class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    recipient_name: str
    recipient_email: str
    course_name: str
    status: str
    file_path: Optional[str] = None
    error_message: Optional[str] = None

class JobStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: str = Field(..., validation_alias="id")
    status: str
    total_count: int
    success_count: int
    failed_count: int
    created_at: datetime
    items: List[ItemResponse]