from enum import Enum


class Events(Enum):
    """
    Типы событий
    """

    Registration = "registration"
    Start = "start"
    Profile = "profile"
    Repeat = "repeat"
    Speciality = "speciality"
    AlreadyTried = "already_tried"
    ContinueTask = "continue_task"
    ResetProgress = "reset_progress"
    DescriptSpeciality = "descript_speciality"
    AnswerType = "answer_type"
    TaskStart = "task_start"
    TaskTry = "task_try"
    SendSolution = "send_solution"
    SaveRepeat = "save_repeat"
    Unclear = "unclear"
    FinishSpeciality = "finish_speciality"
    TaskGrade = "task_grade"
    BotGrade = "bot_grade"
    BotReview = "bot_review"
    Thanks = "thanks"
    DontKnow = "don't know"
    Unclear2 = "unclear 2"
