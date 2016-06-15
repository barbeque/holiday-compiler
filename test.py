import compiler

d = compiler.interpret_relative_date('second friday in april')
assert d.month == 4
assert d.day == 8
