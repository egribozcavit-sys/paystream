from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountCreate(BaseModel):
    user_id: str
    currency: str = Field(default="USD", min_length=3, max_length=3)


class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    account_number: str
    balance_cents: int
    currency: str
    is_active: bool
    created_at: datetime


class TransactionCreate(BaseModel):
    sender_account_id: str
    receiver_account_id: str
    amount_cents: int = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    transaction_type: Literal["transfer"] = "transfer"
    description: str | None = Field(default=None, max_length=1000)
    metadata: dict[str, Any] | None = None


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    sender_account_id: str
    receiver_account_id: str
    amount_cents: int
    currency: str
    status: str
    transaction_type: str
    description: str | None
    idempotency_key: str
    created_at: datetime
    completed_at: datetime | None
    failure_reason: str | None
