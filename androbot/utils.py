import random
import string
from datetime import datetime

from .actions import Actions
from .errors import TooManyParamsForLoggingActions
from .schemas import EventsLog
from .types_ import Events


class Utils:
    @staticmethod
    def get_random_text(num: int) -> str:
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(num))

    @staticmethod
    def get_random_number(num: int) -> str:
        letters = string.digits
        return "".join(random.choice(letters) for i in range(num))


def log_event(tg_user_id: int, event: Events, *args):

    if len(args) > 5:
        raise TooManyParamsForLoggingActions("Can't log more than 5 parameters")

    new_event = EventsLog(tg_user_id=tg_user_id, event_type=event, datetime=datetime.utcnow())

    for i, param in enumerate(args, 1):
        setattr(new_event, f"param{i}", param)

    with Actions() as act:
        act.add_event(new_event)
