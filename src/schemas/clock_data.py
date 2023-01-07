from mongoengine import *

class DeadlineData(EmbeddedDocument):
    practice_id = IntField(required=True)
    reminder_hours_offsets = ListField(DateTimeField)
    final_changes_deadline = DateTimeField(required=True)
    release_time_deadline = DateTimeField(required=True)

class ClockData(EmbeddedDocument):
    final_changes_deadline = IntField(required=True)
    final_changes_deadline_reminder_hours_offset = ListField(IntField)
    release_time_deadline = IntField(required=True)
    deadlines = EmbeddedDocumentListField(DeadlineData)