# Bulk Certificate Generator API 📜

A robust, production-ready FastAPI backend application designed to generate, validate, and manage bulk PDF certificates asynchronously with relational database tracking and fault isolation.

---

## 🌟 Key Features

* **Bulk Certificate Generation**: Submit multiple recipients in a single JSON payload to generate PDF certificates in batches.
* **Fault Isolation**: If one recipient's record contains invalid data or fails, valid certificates are still processed successfully without crashing the batch.
* **Relational Database Storage**: Tracks overall batch job states and individual certificate statuses (`COMPLETED`, `FAILED`, `SUCCESS`) in SQLite via SQLAlchemy.
* **Dynamic PDF Generation**: Automatically renders customized, landscape-oriented PDF certificates complete with borders, vector graphic headers, recipient details, and issue dates using ReportLab.
* **File Retrieval & Download**: Dedicated endpoints allow viewing job progress and downloading generated PDF certificates directly.
* **Interactive UI**: Built-in Swagger UI documentation allows non-technical users to test endpoints directly from their web browser without coding.

---

## 📁 Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py          # FastAPI routes for job creation, status, and PDF download
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py            # SQLite database engine and session configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── job.py                # SQLAlchemy ORM models (CertificateJob & CertificateItem)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── certificate.py        # Pydantic request & response validation schemas
│   └── services/
│       ├── __init__.py
│       └── pdf_generator.py      # ReportLab engine for PDF rendering
│
├── media/                        # Storage folder where generated PDFs are saved
│   └── certificates/
│
├── tests/
│   └── test_main.py              # Integration tests using pytest and FastAPI TestClient
│
├── .gitignore                    # Excludes venv, database files, and media outputs
├── certificates.db               # SQLite database file (auto-generated at runtime)
├── conftest.py                   # Pytest entry configuration
├── main.py                       # Main application entry point
├── README.md                     # Project documentation
└── requirements.txt              # Project dependencies

🚀 Step-by-Step Setup Guide
Follow these steps to set up the project on your machine:

Prerequisites
Python 3.10+ installed on your system.

Git installed on your system.

1. Clone the Repository
Open your terminal (PowerShell or Command Prompt) and clone the repository:

Bash
git clone [https://github.com/maazzafar1234/bulk-certificate-generator.git](https://github.com/maazzafar1234/bulk-certificate-generator.git)
cd bulk-certificate-generator
2. Create and Activate a Virtual Environment
Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install all required libraries using requirements.txt:

Bash
pip install -r requirements.txt
💻 How to Run the Application
Start the live FastAPI server by running:

Bash
python main.py
You will see output indicating that the application server has started:

Plaintext
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
🧪 How to Run Automated Tests
To run the automated test suite and ensure all components (database, routes, and PDF generation) are functioning properly:

Ensure your virtual environment is active.

Run the pytest command:

Bash
python -m pytest
Expected Output:

Plaintext
============================== test session starts ==============================
collected 2 items

tests\test_main.py ..                                                    [100%]

=============================== 2 passed in 0.76s ===============================
📖 How to Generate & Download Certificates (Non-Technical User Guide)
You don't need Postman or code to use this API. You can test and download certificates directly in your browser using the built-in Swagger UI.

Step 1: Open the Interactive Web Page
Start the server using python main.py.

Open your web browser (Chrome, Edge, Safari) and go to:
👉 http://127.0.0.1:8000/docs

Step 2: Submit a Bulk Certificate Generation Request
Locate and click on the POST /api/certificates/generate bar to expand it.

Click the Try it out button located on the top-right corner of that section.

Replace the text in the Request body box with the sample JSON payload below:

📋 Sample JSON Payload:
JSON
{
  "recipients": [
    {
      "recipient_name": "Maaz",
      "recipient_email": "maaz@example.com",
      "course_name": "FastAPI & Backend Engineering",
      "issue_date": "2026-10-07"
    },
    {
      "recipient_name": "Invalid Candidate",
      "recipient_email": "invalid-email-address",
      "course_name": "FastAPI & Backend Engineering",
      "issue_date": "2026-10-07"
    }
  ]
}
Click the blue Execute button.

Step 3: Check the Server Response
Scroll down to the Responses area. You will see a 200 OK response returning a structure like this:

JSON
{
  "status": "COMPLETED",
  "total_count": 2,
  "success_count": 1,
  "failed_count": 1,
  "created_at": "2026-10-07T14:00:00",
  "job_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
  "items": [
    {
      "id": "9f8e7d6c-5b4a-3210-fedc-0987654321ba",
      "recipient_name": "Maaz",
      "recipient_email": "maaz@example.com",
      "course_name": "FastAPI & Backend Engineering",
      "status": "SUCCESS",
      "file_path": "media/certificates/a1b2c3d4/9f8e7d6c.pdf",
      "error_message": null
    },
    {
      "id": "1a2b3c4d-5e6f-7890-abcd-0987654321fe",
      "recipient_name": "Invalid Candidate",
      "recipient_email": "invalid-email-address",
      "course_name": "FastAPI & Backend Engineering",
      "status": "FAILED",
      "file_path": null,
      "error_message": "Invalid recipient email address format"
    }
  ]
}
Notice how Fault Isolation works: Even though "Invalid Candidate" failed due to an invalid email address, "Maaz" succeeded and generated a valid PDF!

Copy the id of the successful item (e.g., 9f8e7d6c-5b4a-3210-fedc-0987654321ba).

Step 4: Download Your Generated PDF Certificate
On the same /docs page, scroll down to the GET /api/certificates/download/{item_id} endpoint and click to expand it.

Click the Try it out button in the top-right corner.

Paste the copied certificate id into the item_id input box.

Click Execute.

Click Download file in the response section to download and open your generated PDF certificate directly in your browser or local PDF reader!

📐 Important Architecture & Design Decisions
Fault Isolation Architecture:

Bulk requests run each recipient through an isolated try-except block during processing.

If a single recipient fails due to invalid parameters or formatting errors, the error is caught, recorded in the database error_message column, and flagged as FAILED.

Remaining valid recipients in the same batch continue processing uninterrupted.

Database Modeling:

Uses two normalized SQL tables: CertificateJob (parent batch) and CertificateItem (individual recipient records).

Ensures standard relational tracking, clean audit trails, and transactional consistency.

Schema Mapping & Pydantic V2 Compatibility:

Uses Pydantic V2 ConfigDict(from_attributes=True) and explicit validation_alias="id" mappings to ensure database primary keys cleanly translate to client-facing response models (job_id and id).

Dynamic Vector PDF Generation:

Utilizes ReportLab's low-level canvas and drawing primitives (reportlab.graphics.shapes) rather than external heavy HTML-to-PDF rendering engines.

Ensures lightweight, high-performance, landscape-oriented PDF generation with precise typography and geometric borders.
