from enum import Enum

class CarpoolCalculationMethod(Enum):
    NO_VARSITY_IN_NOVICE = 1
    VARSITY_IN_NOVICE = 2

class PracticeClassification(Enum):
    PRACTICE_1 = "prac1"
    PRACTICE_2 = "prac2"

class Weekdays(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7