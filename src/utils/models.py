"""Модели для валидации входных данных от бэкенда."""

from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserShort(BaseModel):
    """Усеченная модель пользователя."""

    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id_telegram: Optional[int] = None


class Space(BaseModel):
    """Модель пространства(базы) пользователя."""

    id: int
    name: str
    owner_id: int
    owner_username: str
    linked_chat: str
    available_linked_users: list[UserShort] | None = None


class CoreSettings(BaseModel):
    """Модель базовых настроек пользователя."""

    user: str
    current_space: Space | None
    current_year: int | None = Field(ge=2000, le=2200)
    current_month: int | None = Field(ge=1, le=12)


class CoreSettingsUpdate(BaseModel):
    """Модель для обновления базовых настроек пользователя."""

    current_space_id: int
    current_year: int | None = Field(ge=2000, le=2200)
    current_month: int | None = Field(ge=1, le=12)


class TelegramSettings(BaseModel):
    """Модель Telegram настроек пользователя."""

    user: str
    id_telegram: Optional[int] = None
    telegram_only: bool


class User(BaseModel):
    """Полная модель пользователя."""

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
    """Модель для представления отдельной статьи в суммарном отчете."""

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
    """Модель для представления суммарного отчета."""

    sum_income_plan: Decimal
    sum_income_fact: Decimal
    sum_expense_plan: Decimal
    sum_expense_fact: Decimal
    balance_plan: Decimal
    balance_fact: Decimal
    summary: list[SummaryDetail]


class CreatedGroup(BaseModel):
    """Модель для создания статьи."""

    id: int
    type_transaction: str
    group_name: str
    plan_value: Decimal
    fact_value: Decimal


class Transaction(BaseModel):
    """Модель для транзакции."""

    id: int
    type_transaction: str
    group_name: str
    description: str
    value_transaction: Decimal
    author: int
