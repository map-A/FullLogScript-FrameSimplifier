
from tool_function import *
from graph import *
import ast

a = "NULL"
print(is_macro(a))

s = "C b[2] = (enumerate);"
print(parse_statement(s)) 