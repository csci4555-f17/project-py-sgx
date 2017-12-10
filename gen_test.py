import random, string
from enum import Enum

LINES = 27700

NUM_VARS = 14
vars = []

CONDITION_VARS_NUM = 7
condition_vars = []

ops = ["+", "+-"]

min_ops_per_line = 1
max_ops_per_line = 5

max_int = 100
min_int = -100

class Action(Enum):
	GO_DEEPER = 1
	STAY = 2
	GO_OUT = 3

	@staticmethod
	def get_action(linenum, curr_ident):
		pr = random.uniform(0, 1) + (linenum % 10) * 0.01 + curr_ident * 0.07
		if pr < 0.2:
			return Action.GO_DEEPER
		elif 0.2 <= pr < 0.93:
			return Action.STAY
		else:
			return Action.GO_OUT

for x in range(0, NUM_VARS):
	vars.append(''.join(random.choice(string.ascii_letters) for i in xrange(5)))

linenum = 0
curr_indent_level = 0
code = "_rand_seed_time()\n"
generate_else = False

for i in xrange(CONDITION_VARS_NUM):
	var = "condition_" + str(i)
	#code += var + " = " + str(random.randint(0, 1)) + "\n"
	code += var + " = _rand_zero_or_one()\n"
	condition_vars.append(var)
code += "_nanotime_begin()\n"
for var in vars:
	code += var + " = " + str(random.randint(min_int, max_int)) + "\n"

while linenum < LINES:
	line_ops = random.randint(min_ops_per_line, max_ops_per_line)
	code += "\t" * curr_indent_level
	var = random.choice(vars)
	code += var + " = " + var
	for _ in xrange(line_ops):
		code += " " + random.choice(ops) + " "
		code += random.choice(vars)
	code += "\n"

	action = Action.get_action(linenum=linenum, curr_ident=curr_indent_level)
	if action == Action.GO_OUT:
		if curr_indent_level == 0:
			pass
		else:
			if generate_else:
				code += "\t" * (curr_indent_level - 1) + "else:\n"
				generate_else = False
			else:
				curr_indent_level -= 1
	elif action == Action.STAY:
		pass
	elif action == Action.GO_DEEPER:
		code += "\t" * curr_indent_level
		code += "if " + random.choice(condition_vars) + ":\n"
		curr_indent_level += 1
		# generate_else = True
	linenum += 1

code += "_print_nanotime_diff()\n"
print code