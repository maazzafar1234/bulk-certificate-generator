import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.job import CertificateJob, CertificateItem, JobStatus, ItemStatus
from app.schemas.certificate import BulkCertificateRequest, JobStatusResponse
from app.services.pdf_generator import generate_pdf_certificate

router = APIRouter()

@router.post("/certificates/generate", response_model=JobStatusResponse)
def generate_bulk_certificates(payload: BulkCertificateRequest, db: Session = Depends(get_db)):
    if not payload.recipients:
        raise HTTPException(status_code=400, detail="Recipient list cannot be empty.")

    job = CertificateJob(total_count=len(payload.recipients))
    db.add(job)
    db.commit()
    db.refresh(job)

    for item_data in payload.recipients:
        item = CertificateItem(
            job_id=job.id,
            recipient_name=item_data.recipient_name,
            recipient_email=item_data.recipient_email,
            course_name=item_data.course_name,
            issue_date=item_data.issue_date
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        try:
            # Simulated individual error check
            if "invalid" in item_data.recipient_name.lower():
                raise ValueError("Generation failed for invalid recipient name.")

            file_path = os.path.join("media", "certificates", str(job.id), f"{item.id}.pdf")
            generate_pdf_certificate(
                recipient_name=item_data.recipient_name,
                course_name=item_data.course_name,
                issue_date=item_data.issue_date,
                output_path=file_path
            )

            item.status = ItemStatus.SUCCESS
            item.file_path = file_path
            job.success_count += 1

        except Exception as err:
            item.status = ItemStatus.FAILED
            item.error_message = str(err)
            job.failed_count += 1

        db.commit()

    job.status = JobStatus.COMPLETED
    db.commit()
    db.refresh(job)

    return job

@router.get("/certificates/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(CertificateJob).filter(CertificateJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job

@router.get("/certificates/download/{item_id}")
def download_certificate(item_id: str, db: Session = Depends(get_db)):
    item = db.query(CertificateItem).filter(CertificateItem.id == item_id).first()
    if not item or item.status != ItemStatus.SUCCESS:
        raise HTTPException(status_code=404, detail="Certificate not generated or job failed.")
    
    if not os.path.exists(item.file_path):
        raise HTTPException(status_code=404, detail="File missing on server disk.")

    return FileResponse(
        path=item.file_path, 
        filename=f"{item.recipient_name.replace(' ', '_')}_Certificate.pdf", 
        media_type="application/pdf"
    )