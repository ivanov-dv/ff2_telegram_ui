from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Space(BaseModel):
    id: int
    name: str

class CoreSettings(BaseModel):
    user: str
    current_space: Space
    current_year: int = Field(ge=2000, le=2200)
    current_month: int = Field(ge=1, le=12)

class TelegramSettings(BaseModel):
    user: str
    id_telegram: Optional[int]
    telegram_only: bool
    joint_chat: Optional[str]


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
    spaces: Optional[List[Space]] = None
