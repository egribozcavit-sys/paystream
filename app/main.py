from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import accounts, auth, transactions, users
from app.config import settings
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="A.S.A.S. Cloud API",
    version="1.0.0",
    description="Development payment-ledger demonstration API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {
        "service": "A.S.A.S. Cloud API",
        "status": "operational",
        "environment": settings.environment,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
