from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserShort(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id_telegram: Optional[int] = None


class Space(BaseModel):
    id: int
    name: str
    owner_id: int
    owner_username: str
    linked_chat: str
    available_linked_users: list[UserShort] | None = None


class CoreSettings(BaseModel):
    user: str
    current_space: Space | None
    current_year: int | None = Field(ge=2000, le=2200)
    current_month: int | None = Field(ge=1, le=12)


class CoreSettingsUpdate(BaseModel):
    current_space_id: int
    current_year: int | None = Field(ge=2000, le=2200)
    current_month: int | None = Field(ge=1, le=12)


class TelegramSettings(BaseModel):
    user: str
    id_telegram: Optional[int] = None
    telegram_only: bool


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_joined: Optional[datetime] = None
    last_login: Optional[datetime] = None
    core_settings: Optional[CoreSettings] = None
    telegram_settings: Optional[TelegramSettings] = None
    spaces: Optional[list[Space]] = None
    available_linked_spaces: Optional[list[Space]] = None


class SummaryDetail(BaseModel):
    id: int
    space: Space
    period_month: int
    period_year: int
    type_transaction: str
    group_name: str
    plan_value: Decimal
    fact_value: Decimal
    created_at: datetime
    updated_at: datetime


class Summary(BaseModel):
    sum_income_plan: Decimal
    sum_income_fact: Decimal
    sum_expense_plan: Decimal
    sum_expense_fact: Decimal
    balance_plan: Decimal
    balance_fact: Decimal
    summary: list[SummaryDetail]


class CreatedGroup(BaseModel):
    id: int
    type_transaction: str
    group_name: str
    plan_value: Decimal
    fact_value: Decimal


class Transaction(BaseModel):
    id: int
    type_transaction: str
    group_name: str
    description: str
    value_transaction: Decimal
    author: int
