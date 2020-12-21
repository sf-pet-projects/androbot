import random
import string


class Utils:
    @staticmethod
    def get_random_text(num: int) -> str:
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(num))

    @staticmethod
    def get_random_number(num: int) -> str:
        letters = string.digits
        return "".join(random.choice(letters) for i in range(num))
