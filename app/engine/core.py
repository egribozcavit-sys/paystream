import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Account, AuditLog, Transaction


@dataclass
class TransactionTask:
    sender_account_id: str
    receiver_account_id: str
    amount_cents: int
    currency: str
    transaction_type: str
    description: str
    metadata: dict
    idempotency_key: str
    created_at: str


class TransactionEngine:
    def submit_transaction(self, task: TransactionTask) -> str:
        with SessionLocal() as db:
            existing = db.scalar(
                select(Transaction).where(
                    Transaction.idempotency_key == task.idempotency_key
                )
            )
            if existing:
                return existing.id

            transaction = Transaction(
                sender_account_id=task.sender_account_id,
                receiver_account_id=task.receiver_account_id,
                amount_cents=task.amount_cents,
                currency=task.currency.upper(),
                transaction_type=task.transaction_type,
                description=task.description,
                transaction_metadata=task.metadata,
                idempotency_key=task.idempotency_key,
                status="processing",
            )
            db.add(transaction)

            try:
                self._apply_transfer(db, transaction)
                db.commit()
            except Exception:
                db.rollback()
                raise

            return transaction.id

    def _apply_transfer(self, db: Session, transaction: Transaction) -> None:
        if transaction.sender_account_id == transaction.receiver_account_id:
            transaction.status = "failed"
            transaction.failure_reason = "sender_and_receiver_must_differ"
            return

        sender = db.scalar(
            select(Account)
            .where(Account.id == transaction.sender_account_id)
            .with_for_update()
        )
        receiver = db.scalar(
            select(Account)
            .where(Account.id == transaction.receiver_account_id)
            .with_for_update()
        )

        if sender is None or receiver is None:
            transaction.status = "failed"
            transaction.failure_reason = "account_not_found"
            return

        if not sender.is_active or not receiver.is_active:
            transaction.status = "failed"
            transaction.failure_reason = "inactive_account"
            return

        if sender.currency != transaction.currency or receiver.currency != transaction.currency:
            transaction.status = "failed"
            transaction.failure_reason = "currency_mismatch"
            return

        if sender.balance_cents < transaction.amount_cents:
            transaction.status = "failed"
            transaction.failure_reason = "insufficient_balance"
            return

        sender.balance_cents -= transaction.amount_cents
        receiver.balance_cents += transaction.amount_cents

        transaction.status = "completed"
        transaction.completed_at = datetime.now(timezone.utc)

        db.add(
            AuditLog(
                transaction_id=transaction.id,
                user_id=sender.user_id,
                action="transfer_completed",
                details={
                    "amount_cents": transaction.amount_cents,
                    "currency": transaction.currency,
                    "sender_account_id": sender.id,
                    "receiver_account_id": receiver.id,
                },
            )
        )


engine = TransactionEngine()
