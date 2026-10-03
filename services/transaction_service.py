import time
from datetime import datetime, timezone

from app.engine.core import TransactionTask, engine
from app.models import Account, Transaction
from app.schemas import TransactionCreate
from services.base import BaseService


class TransactionService(BaseService[Transaction]):
    def create_transaction(
        self,
        transaction_data: TransactionCreate,
        idempotency_key: str | None = None,
    ) -> dict:
        key = idempotency_key or f"auto-{time.time_ns()}"

        existing = (
            self.db.query(Transaction)
            .filter(Transaction.idempotency_key == key)
            .first()
        )
        if existing is not None:
            return {
                "status": existing.status,
                "transaction_id": existing.id,
                "duplicate": True,
            }

        sender = self.db.get(Account, transaction_data.sender_account_id)
        receiver = self.db.get(Account, transaction_data.receiver_account_id)

        if sender is None or receiver is None:
            raise ValueError("Invalid account(s)")

        task = TransactionTask(
            sender_account_id=transaction_data.sender_account_id,
            receiver_account_id=transaction_data.receiver_account_id,
            amount_cents=transaction_data.amount_cents,
            currency=transaction_data.currency.upper(),
            transaction_type=transaction_data.transaction_type,
            description=transaction_data.description or "",
            metadata=transaction_data.metadata or {},
            idempotency_key=key,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        transaction_id = engine.submit_transaction(task)

        transaction = self.db.get(Transaction, transaction_id)
        return {
            "status": transaction.status if transaction else "unknown",
            "transaction_id": transaction_id,
            "duplicate": False,
        }

    def get_transaction(self, transaction_id: str) -> Transaction:
        transaction = self.db.get(Transaction, transaction_id)
        if transaction is None:
            raise ValueError("Transaction not found")
        return transaction
