from mongoengine import *
from schemas.user_data import UserData
from schemas.practice_schedule_data import PracticeScheduleData
from schemas.clock_data import ClockData
from schemas.carpool_history_data import CarpoolHistoryData

class TermData(Document):
    term_num = IntField(required=True)
    user_data = EmbeddedDocumentListField(UserData)
    practice_schedule_data = EmbeddedDocumentListField(PracticeScheduleData)
    clock_data = EmbeddedDocumentListField(ClockData)
    carpool_history_data = EmbeddedDocumentListField(CarpoolHistoryData)
