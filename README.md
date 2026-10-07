# Bulk Certificate Generator API

## Overview
FastAPI backend built to process bulk certificate generation requests synchronously, track overall job and recipient progress, handle individual errors independently, and serve PDF certificate downloads.

## Design Decisions
- **Synchronous Processing**: Chosen for simplicity and direct execution without requiring external message queue dependencies (like Redis/Celery).
- **Fault Isolation**: Each recipient in a batch is executed in an isolated try-except block, ensuring individual item failures do not halt generation of other valid items.

## Setup & Running on Windows

1. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1