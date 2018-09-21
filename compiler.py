import calendar, datetime

def compile(source_path, year = datetime.datetime.now().year):
    output = []

    with open(source_path.strip(), 'r') as fp:
        for raw_line in fp.readlines():
            # clean up the input line
            line = clean_line(raw_line)
            if len(line) < 1:
                continue
            print line

            # does it look like an import statement?
            if line.startswith("#"):
                # parse the next few lines...
                if line.startswith("#include"):
                    tokens = line.split()
                    # TODO: error checking...
                    to_import = tokens[1]
                    imported_items = compile(to_import, year)
                    output.extend(imported_items)
                else:
                    raise ValueError("I have no idea what this compiler directive is", line)
                continue

            # does it look like an absolute date?
            if looks_like_absolute_date(line):
                output.append(interpret_absolute_date(line, year))
                continue
            
            # does it look like a relative date?
            try:
                rel_date = interpret_relative_date(line, year)
                output.append(rel_date)
            except ValueError:
                print "Could not parse line", raw_line

    return output

def clean_line(raw_line):
    """
    Strips comments and generally cleans up a line, preparing it for
    tokenization.
    """
    return raw_line.partition("//")[0].strip()

def looks_like_absolute_date(line):
    if line.lower() == "easter":
        return True
    tokens = line.split()
    if is_valid_month(tokens[0].strip()):
        return True
    return False

def interpret_absolute_date(datestring, year):
    """
    Converts an absolute date like 'december 11' into a datetime.
    """
    if datestring.lower() == "easter":
        return get_easter_for(year)

    tokens = datestring.split()
    return datetime.date(year, month_name_to_number(tokens[0]),
                         int(tokens[1]))

def interpret_relative_date(relative, year):
    """
    Interprets a relative date, such as "second monday of april"
    """
    tokens = relative.split()
    
    if len(tokens) != 4:
        raise ValueError("Wrong number of tokens to be a relative date")

    which_occurrence = convert_nth_to_number(tokens[0])
    which_day_of_week = tokens[1].lower()

    # third token could be 'of' or 'in', do we need to rule lawyer this one?

    which_month = tokens[3]

    # start counting throughout the month
    remaining_reps = which_occurrence
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
            day = day + 7 # skip a week to cut on the reps...
        else:
            day = day + 1

def month_name_to_number(month_name):
    """
    Converts a human readable month name into a 1-indexed
    integer of what month number it is for.
    """
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
    } # todo: shortmonths

    if month_name.strip().lower() in mapping:
        return mapping[month_name.strip().lower()]
    else:
        raise ValueError("Invalid month: '{}'".format(month_name))

def is_valid_month(maybe_month):
    try:
        month_name_to_number(maybe_month)
        return True
    except ValueError:
        return False

def day_of_week_at(day, month, year):
    """
    Determines what weekday a given date falls on.
    """
    return datetime.date(year,month,day).strftime("%A").lower()

def get_easter_for(year):
    a = year % 19
    b = year / 100
    c = year % 100
    d = b / 4
    e = b % 4
    f = (b + 8) / 25
    g = (b - f + 1) / 3
    h = (19 * a + b - d - g + 15) % 30
    i = c / 4
    k = c % 4
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) / 451
    month = (h + L - 7 * m + 114) / 31
    day = ((h + L - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)
    
# convert 'first', 'second', 'third' to numbers?
def convert_nth_to_number(nth_token):
    nth_dict = { 'first': 0, 'second': 1, 'third': 2, 'fourth': 3 }
    if nth_token.lower() in nth_dict:
        return nth_dict[nth_token.lower()]
    else:
        raise ValueError("The token '{}' is not understood as an ordinal here.".format(nth_token))
