import sys

from androbot import models
from androbot.actions import Actions
from androbot.database import engine
from androbot.types_ import Specialty

models.Base.metadata.create_all(bind=engine)

if len(sys.argv) < 2:
    print("You're must specify filename in command line")

with Actions() as act:
    act.load_questions(specialty=Specialty.ANDROID, file=sys.argv[1])
