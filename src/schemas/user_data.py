from mongoengine import *
from schemas.enums import Weekdays

class AddressData(EmbeddedDocument):
    number = IntField(required=True)
    street = StringField(required=True)
    city = StringField(required=True)
    hidden = BooleanField(required=True, default=True)

class CarData(EmbeddedDocument):
    num_seats = IntField(required=True)
    description = StringField(required=True)
    hidden = BooleanField(required=True, default=True)

class UserData(EmbeddedDocument):
    user_id = IntField(required=True)
    prac1_availability = ListField(EnumField(Weekdays))
    prac2_availability = ListField(EnumField(Weekdays))
    address_data = EmbeddedDocumentField(AddressData)
    car_data = EmbeddedDocumentField(CarData, default=None)