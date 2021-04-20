from enum import Enum


class UserScore(Enum):
    WRONG = 0, "Неверный"
    PARTLY = 1, "Частично верный"
    RIGHT = 2, "Верный"

    def __init__(self, value: int, description: str = None):
        self._value_ = value
        self._description_ = description

    @property
    def description(self):
        return self._description_

    @classmethod
    def by_description(cls, find_description: str) -> Enum:
        matched = [x for x in UserScore if x.description.lower() in find_description.lower()]
        if matched:
            return matched[0]
        else:
            return UserScore.WRONG
