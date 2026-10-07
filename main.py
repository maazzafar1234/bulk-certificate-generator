from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.endpoints import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulk Certificate Generator API")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)