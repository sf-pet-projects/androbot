from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class TelegramUserBase(BaseModel):
    tg_user_id: int
    name: str
    username: str
    specialty: str


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
    id: int
    question_type: str
    text_question: str
    text_answer: str

    class Config:
        orm_mode = True


class CurrentSession(BaseModel):
    quest_id: int
    tg_user_id: int

    class Config:
        orm_mode = True
