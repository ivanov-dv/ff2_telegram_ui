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
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_joined: Optional[datetime]
    last_login: Optional[datetime]
    core_settings: Optional[CoreSettings]
    telegram_settings: Optional[TelegramSettings]
    spaces: Optional[List[Space]]


if __name__ == '__main__':

    d = {
        "id": 2,
        "username": "regular-use",
        "email": "",
        "first_name": "",
        "last_name": "",
        "date_joined": "2024-12-05T13:12:55.592012Z",
        "last_login": None,
        "core_settings": {
            "user": "regular-use",
            "current_space": {
                "id": 1,
                "name": "regular-use"
            },
            "current_month": 12,
            "current_year": 2024
        },
        "telegram_settings": {
            "user": "regular-use",
            "id_telegram": 777,
            "telegram_only": True,
            "joint_chat": None
        },
        "spaces": [
            {
                "id": 1,
                "name": "regular-use"
            }
        ]
    }


    user = User(**d)
    print(user)