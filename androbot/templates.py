import aiogram.types as aiotypes


def render_message(template_text: str, message: aiotypes.Message):
    parsed_text = template_text.format(username=message.from_user.username)
    return parsed_text
