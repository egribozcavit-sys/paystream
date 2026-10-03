from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionRead
from services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_transaction(
    payload: TransactionCreate,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    db: Session = Depends(get_db),
):
    try:
        return TransactionService(db).create_transaction(
            payload,
            idempotency_key=idempotency_key,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction = db.get(Transaction, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction_not_found")
    return transaction
