import compiler
import datetime

d = compiler.interpret_relative_date('second friday in april', 2016)
assert d.month == 4
assert d.day == 8

# easter test
d = compiler.get_easter_for(2016)
print 'easter=', d
assert d.year == 2016
assert d.month == 3
assert d.day == 27

# read the file in
this_year = datetime.datetime.now().year

dates = []

for year in range(this_year, this_year + 10):
    print 'generating dates for', year
    dates.extend(compiler.compile("alberta.hc", year))

with open('dates.csv', 'w') as out:
    for date in dates:
        out.write(date.strftime("%Y-%m-%d") + "\n")
