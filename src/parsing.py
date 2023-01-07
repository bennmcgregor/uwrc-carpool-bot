import csv
from io import StringIO
from custom_errors import CommandValidationError
from schemas.enums import Weekdays, PracticeClassification
from datetime import datetime

def parse_prac1_prac2_weekdays(availability):
    prac1_weekdays = set()
    prac2_weekdays = set()
    i = 0
    try:
        tokens = availability.split(" ")
        if tokens[i] == "prac1":
            i += 1
            if tokens[i] != "prac2":
                for num in tokens[i]:
                    weekday = Weekdays(int(num))
                    prac1_weekdays.add(weekday)
                i += 1
            if tokens[i] == "prac2":
                i += 1
                if i < len(tokens):
                    for num in tokens[i]:
                        weekday = Weekdays(int(num))
                        prac2_weekdays.add(weekday)
                
                return list(prac1_weekdays), list(prac2_weekdays)
    except:
        pass
    raise CommandValidationError()

def parse_single_date(date):
    practices = set()
    try:
        tokens = date.split(" ")
        date = datetime.strptime(tokens[0],'%d%m%y')
        if len(tokens) > 1:
            practices.add(PracticeClassification(tokens[1][:5]))
            if len(tokens[1]) > 5:
                practices.add(PracticeClassification(tokens[1][5:]))
            return date, list(practices)
    except:
        pass
    raise CommandValidationError()

def parse_multiple_dates(dates):
    date_list = []
    tokens = dates.split(" ")
    for date in [" ".join(tokens[i:i+2]) for i in range(0, len(tokens), 2)]:
        date_list.append(parse_single_date(date))
    return date_list

def parse_csv(csv_string):
    data = []
    try:
        f = StringIO(csv_string.replace(";", "\n"))
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            prac_time = datetime.strptime(row[0],'%d%m%y-%H:%M:%S')
            prac_class = PracticeClassification(row[1])
            if row[2] in ["y", "n"]:
                carpool = row[2] == "y"
            else:
                raise CommandValidationError()
            data.append((prac_time, prac_class, carpool))
        
        return data
    except:
        pass
    raise CommandValidationError()

def parse_reminders(hours_before_release, reminder_offsets):
    reminders = set()
    try:
        for offset in reminder_offsets.split(" "):
            offset = int(offset)
            if offset >= hours_before_release:
                raise CommandValidationError()
            reminders.add(offset)

        reminders_list = list(reminders)
        reminders_list.sort()
        return reminders_list
    except:
        pass
    raise CommandValidationError()