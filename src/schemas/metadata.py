from mongoengine import *
from schemas.enums import CarpoolCalculationMethod

class MetaData(Document):
    carpool_calculation_method = EnumField(CarpoolCalculationMethod, default = CarpoolCalculationMethod.NO_VARSITY_IN_NOVICE)
    current_term_num = IntField()