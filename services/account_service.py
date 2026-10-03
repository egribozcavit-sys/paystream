import uuid

from app.models import Account
from app.schemas import AccountCreate
from services.base import BaseService


class AccountService(BaseService[Account]):
    def create_account(self, account_data: AccountCreate) -> Account:
        account = Account(
            user_id=account_data.user_id,
            account_number=str(uuid.uuid4()),
            currency=account_data.currency.upper(),
            balance_cents=0,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_account_by_id(self, account_id: str) -> Account:
        account = self.db.get(Account, account_id)
        if account is None:
            raise ValueError("Account not found")
        return account

    def get_balance(self, account_id: str) -> int:
        return self.get_account_by_id(account_id).balance_cents
