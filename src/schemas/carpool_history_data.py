from mongoengine import *

class CarpoolData(EmbeddedDocument):
    driver_user_id = IntField(required=True)
    passengers = ListField(IntField)

class CarpoolHistoryData(EmbeddedDocument):
    practice_id = IntField(required=True)
    datetime = DateTimeField(required=True)
    carpools = EmbeddedDocumentListField(CarpoolData)