from typing import Union

import aiogram.types as aiotypes


def render_message(template_text: str, message: Union[aiotypes.Message, aiotypes.CallbackQuery]):
    parsed_text = template_text.replace("{{username}}", message.from_user.username)
    return parsed_text
