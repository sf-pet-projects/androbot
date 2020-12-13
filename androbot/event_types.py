from enum import Enum


class Events(Enum):
    registration = ("registration",)
    start = ("start",)
    profile = ("profile",)
    repeat = ("repeat",)
    speciality = ("speciality",)
    already_tried = ("already_tried",)
    continue_task = ("continue_task",)
    reset_progress = ("reset_progress",)
    descript_speciality = ("descript_speciality",)
    answer_type = ("answer_type",)
    task_start = ("task_start",)
    task_try = ("task_try",)
    send_solution = ("send_solution",)
    save_repeat = ("save_repeat",)
    unclear = ("unclear",)
    finish_speciality = ("finish_speciality",)
    task_grade = ("task_grade",)
    bot_grade = ("bot_grade",)
    bot_review = ("bot_review",)
    thanks = "thanks"
