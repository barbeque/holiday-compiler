import calendar, datetime

# interprets a relative date, like "second monday of april"

def interpret_relative_date(relative):
    tokens = relative.split()
    
    if len(tokens) != 4:
        raise ValueError("Wrong number of tokens to be a relative date")

    which_occurrence = convert_nth_to_number(tokens[0])
    which_day_of_week = tokens[1].lower()

    # third token could be 'of' or 'in', do we need to rule lawyer this one?

    which_month = tokens[3]

    # start counting throughout the month
    remaining_reps = which_occurrence
    year = 2016 # todo
    month_number = month_name_to_number(which_month)
    day = 1
    while remaining_reps >= 0:
        weekday = day_of_week_at(day, month_number, year)
        if weekday == which_day_of_week:
            # found the weekday for this week
            remaining_reps = remaining_reps - 1
            if remaining_reps < 0:
                # found the target
                return datetime.date(year, month_number, day)
        day = day + 1

def month_name_to_number(month_name):
    mapping = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }

    if month_name.lower() in mapping:
        return mapping[month_name.lower()]
    else:
        raise ValueError("Invalid month: '{0}'" % (month_name))

def day_of_week_at(day, month, year):
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return weekdays[datetime.date(year, month, day).weekday()]
    
# convert 'first', 'second', 'third' to numbers?
def convert_nth_to_number(nth_token):
    nth_dict = { 'first': 0, 'second': 1, 'third': 2, 'fourth': 3 }
    if nth_token.lower() in nth_dict:
        return nth_dict[nth_token.lower()]
    else:
        raise ValueError("The token '{0}' is not understood as an ordinal here.").format(nth_token)
