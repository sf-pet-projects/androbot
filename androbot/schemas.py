from typing import Optional

from pydantic import BaseModel
from pydantic.schema import datetime

from androbot.types_.event_ import Events


class TelegramUserBase(BaseModel):
    tg_user_id: int
    name: str
    username: str
    specialty: Optional[str]


class TelegramUser(TelegramUserBase):
    class Config:
        orm_mode = True


class Answer(BaseModel):
    quest_id: int
    tg_user_id: int
    answer_type: str
    text_answer: Optional[str]
    link_to_audio_answer: Optional[str]

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: Optional[int] = None
    question_type: str
    question_category: Optional[str]
    text_question: Optional[str]
    text_answer: str
    additional_info: Optional[str]

    class Config:
        orm_mode = True


class CurrentSession(BaseModel):
    quest_id: int
    tg_user_id: int

    class Config:
        orm_mode = True


class EventsLog(BaseModel):
    tg_user_id: int
    event_type: Events
    datetime: datetime
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]

    class Config:
        orm_mode = True
