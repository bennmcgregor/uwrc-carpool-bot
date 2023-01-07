from mongoengine import *
from schemas.enums import PracticeClassification

class PracticeScheduleData(EmbeddedDocument):
    id = IntField(required=True)
    datetime = DateTimeField(required=True)
    classification = EnumField(PracticeClassification)
    attending = ListField(IntField)
    driving = ListField(IntField)