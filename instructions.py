import compiler
from abi import abi
from allocator import allocate

ZIGZAG = True

caller_save_regs = {
	"%eax",
	"%edx"
}

callee_save_regs = {
	"%edi",
	"%esi"
}

regs = caller_save_regs | callee_save_regs

reserved_regs = {
	"%esp",
	"%ebp"
}

class UninitializedPadding(RuntimeError):
	pass

class x86instruction(object):
	def __init__(self):
		self.instr = ""

		# which registers does this instruction has side effect on
		self.affected_registers = []

		# vars are either Const, Name, AssName, or str. First 3 are evaluated, last one is copied to var_locations as is
		self.vars = []

		# var_locations are x86 locations($1, %ebp, %eax etc.) corresponding to vars with same index
		self.var_locations = []

		self.live_vars_after = set()

	def __str__(self):
		sstr = self.instr
		for i in range(len(self.vars)):
			sstr += " " + self.vars[i].__repr__()
			if i < len(self.var_locations):
				sstr += "(" + self.var_locations[i] + ")"
		# if len(self.affected_registers) > 0:
		# 	sstr += " {affects" + self.affected_registers.__str__() + "}"
		# sstr += " {live: " + ", ".join(self.live_vars_after) + "}"
		return sstr

	def __repr__(self):
		return str(self)

	def assign_locations(self, all_locations):
		# type: (dict) -> ()
		self.var_locations = []
		for i in range(len(self.vars)):
			if isinstance(self.vars[i], compiler.ast.Const):
				self.var_locations.append("$" + str(self.vars[i].value))
			elif isinstance(self.vars[i], compiler.ast.Name):
				self.var_locations.append(all_locations[self.vars[i].name])
			else:
				self.var_locations.append(self.vars[i])

	def get_x86(self):
		# type () -> str
		return self.instr + " " + ", ".join(self.var_locations)

	# returns names of vars and registers, w/o consts
	# if i is not None, get i'th element, if it exists
	def vars_names(self, i=None):
		# type() -> list[str]
		res = []
		curr_i = 0
		for var in self.vars:
			curr_elem = None
			if isinstance(var, compiler.ast.Name):
				curr_elem = var.name
			elif isinstance(var, str):
				curr_elem = var
			if curr_i == i:
				if curr_elem is None:
					return []
				else:
					return [curr_elem]
			curr_i += 1

			if curr_elem is not None:
				res.append(curr_elem)
		return res

	def is_mem_to_mem(self):
		# type: (str, str) -> bool
		'''
		Returns True if both n1 and n2 are memory pointers.
		Since direct memory-to-memory moves/adds/etc are not allowed, we have to check, and do it via tmp vars.
		'''
		if len(self.var_locations) < 2:
			return False
		return (self.var_locations[0].endswith("p)") or self.var_locations[0].endswith("p")) and\
			   (self.var_locations[1].endswith("p)") or self.var_locations[1].endswith("p"))

	def vars_written(self):
		return []

	def vars_read(self):
		return []

class movl(x86instruction):
	def __init__(self, left_var, right_var):
		super(movl, self).__init__()
		self.instr = "movl"
		self.vars = [left_var, right_var]

	def vars_written(self):
		return self.vars_names(1)

	def vars_read(self):
		return self.vars_names(0)

class unspillableMovl(movl):
	def __str__(self):
		return "(unspillable) " + super(unspillableMovl, self).__str__()


class addl(x86instruction):
	def __init__(self, left_var, right_var):
		super(addl, self).__init__()
		self.instr = "addl"
		self.vars = [left_var, right_var]

	def vars_written(self):
		return self.vars_names(1)

	def vars_read(self):
		return self.vars_names()

class negl(x86instruction):
	def __init__(self, var):
		super(negl, self).__init__()
		self.instr = "negl"
		self.vars = [var]

	def vars_written(self):
		return self.vars_names()

	def vars_read(self):
		return self.vars_names()

class call(x86instruction):
	def __init__(self, instr):
		super(call, self).__init__()
		self.instr = "call " + abi.label(instr)
		self.vars = []
		self.affected_registers = ["%eax"]

	def vars_written(self):
		return self.affected_registers

	def vars_read(self):
		return []


class pushl(x86instruction):
	def __init__(self, var):
		super(pushl, self).__init__()
		self.instr = "pushl"
		self.vars = [var]

	def vars_written(self):
		return []

	def vars_read(self):
		return self.vars_names()

class pad_args(x86instruction):
	"""
	Changes a call to conform to the Application Binary Interface of the
	current OS.
	"""
	def __init__(self, bytes_for_params):
		super(pad_args, self).__init__()
		self.instr = "subl"
		self.padding = None
		self.bytes_for_params = bytes_for_params
		self.vars = [compiler.ast.Const(self.padding), "%esp"]

	def calc_padding(self, bytes_used):
		self.padding = abi.padding_before_call(bytes_used, self.bytes_for_params)
		self.vars[0].value = self.padding

	def vars_written(self):
		return []

	def vars_read(self):
		return self.vars_names()

	def get_x86(self):
		# type () -> str
		if self.padding is None:
			raise UninitializedPadding("`calc_padding` was never called")
		return super(pad_args, self).get_x86()

class unpad_args(x86instruction):
	def __init__(self, pad_instr):
		super(unpad_args, self).__init__()
		self.instr = "addl"
		self.pad_instr = pad_instr
		self.vars = pad_instr.vars

	def vars_written(self):
		return []

	def vars_read(self):
		return self.vars_names()

class if_instr(x86instruction):
	def __init__(self, test_, then_, else_):
		# type (Name, [x86instruction], [x86instruction])
		super(if_instr, self).__init__()
		self.instr = "if"
		self.vars = [test_]
		self.then_ = then_
		self.else_ = else_
		self.affected_registers = ["%eax", "%ecx"]  # al, cl

	def assign_locations(self, all_locations):
		# type: (dict) -> ()
		super(if_instr, self).assign_locations(all_locations)
		for instr in self.then_:
			instr.assign_locations(all_locations)
		for instr in self.else_:
			instr.assign_locations(all_locations)

	def get_x86(self):
		# type () -> str
		lname = allocate().name[10:]
		else_label = "elselabel_" + lname
		end_label = "endlabel_" + lname
		if ZIGZAG:
			start_label = "start_" + lname
			startj_label = start_label + ".j"
			then_label = "thenlabel_" + lname
			thenj_label = then_label + ".j"
			trampoline_to_thenj = "zz" + lname + "_thenj"
			trampoline_to_ebx = "zz" + lname + "_ebx"

			x86str = "# trampoline " + lname + "\n"
			x86str += "jmp " + start_label + "\n" # change from original zigzagger
			x86str += trampoline_to_thenj + ": jmp " + thenj_label + "\n"
			x86str += trampoline_to_ebx + ": jmp *%ebx\n"
			# TODO: cmpl, movl etc from zigzagging should be stored rather than
			# just added to x86 string to be able to reason about it for const-time compilation
			x86str += start_label + ":\n"
			x86str += "movl $" + then_label + ", %ebx\n"
			x86str += "movl $" + else_label + ", %ecx\n"
			x86str += "cmp $0, " + self.var_locations[0] + "\n"
			#x86str += "cmove $" + else_label + ", %ebx\n"
			x86str += "cmove %ecx, %ebx\n"
			x86str += startj_label + ":\njmp " + trampoline_to_thenj + "\n"
			x86str += then_label + ":\n"
			for instr in self.then_:
				x86str += instr.get_x86() + "\n"
			x86str += "movl $" + end_label + ", %ebx\n"
			x86str += thenj_label + ":\njmp " + trampoline_to_ebx + "\n"
			x86str += else_label + ":\n"
			for instr in self.else_:
				x86str += instr.get_x86() + "\n"
			x86str += end_label + ":\n"
		else:
			x86str = "cmpl $0, " + self.var_locations[0] + "\n"
			x86str += "je " + else_label + "\n"
			for instr in self.then_:
				x86str += instr.get_x86() + "\n"
			x86str += "jmp " + end_label + "\n"
			x86str += else_label + ":\n"
			for instr in self.else_:
				x86str += instr.get_x86() + "\n"
			x86str += end_label + ":\n"
		return x86str

	def vars_written(self):
		return self.affected_registers

	def vars_read(self):
		return self.vars_names()

	def __str__(self):
		res = super(if_instr, self).__str__() + "\n"
		res += "| then\n"
		for instr in self.then_:
			res += "|-" + instr.__str__() + "\n"
		res += "| else\n"
		for instr in self.else_:
			res += "|-" + instr.__str__() + "\n"
		res += "|----------" + super(if_instr, self).__str__() + "----------|"
		return res

class cmpl(x86instruction):
	def __init__(self, left, right):
		# type (Bop)
		super(cmpl, self).__init__()
		self.instr = "cmpl"
		self.vars = [left, right]

	def vars_written(self):
		return []

	def vars_read(self):
		return self.vars_names()

class sall(x86instruction):
	def __init__(self, shift, var):
		# shift has to be const
		super(sall, self).__init__()
		self.instr = "sall"
		self.vars = [shift, var]

	def vars_written(self):
		return self.vars_names()

	def vars_read(self):
		return self.vars_names()

class orl(x86instruction):
	def __init__(self, left, right):
		super(orl, self).__init__()
		self.instr = "orl"
		self.vars = [left, right]

	def vars_written(self):
		return self.vars_names(1)

	def vars_read(self):
		return self.vars_names()

class andl(x86instruction):
	def __init__(self, left, right):
		super(andl, self).__init__()
		self.instr = "andl"
		self.vars = [left, right]

	def vars_written(self):
		return self.vars_names(1)

	def vars_read(self):
		return self.vars_names()

class sarl(x86instruction):
	def __init__(self, shift, var):
		# shift has to be const
		super(sarl, self).__init__()
		self.instr = "sarl"
		self.vars = [shift, var]

	def vars_written(self):
		return self.vars_names()

	def vars_read(self):
		return self.vars_names()

class sete_cl(x86instruction):
	def __init__(self):
		super(sete_cl, self).__init__()
		self.instr = "sete %cl"
		self.affected_registers = ["%ecx"]  # cl

	def vars_written(self):
		return self.affected_registers

class setne_cl(x86instruction):
	def __init__(self):
		super(setne_cl, self).__init__()
		self.instr = "setne %cl"
		self.affected_registers = ["%ecx"]  # cl

	def vars_written(self):
		return self.affected_registers

class movzbl_cl(x86instruction):
	def __init__(self, var):
		super(movzbl_cl, self).__init__()
		self.instr = "movzbl %cl,"
		self.vars = [var]

	def vars_written(self):
		return self.vars_names()

	def vars_read(self):
		return []

class cmove(x86instruction):
	def __init__(self, left, right):
		super(cmove, self).__init__()
		self.instr = "cmove"
		self.vars = [left, right]

	def vars_written(self):
		return self.vars_names(1)

	def vars_read(self):
		return self.vars_names(0)

class cmovne(x86instruction):
	def __init__(self, left, right):
		super(cmovne, self).__init__()
		self.instr = "cmovne"
		self.vars = [left, right]

	def vars_written(self):
		return self.vars_names(1)

	def vars_read(self):
		return self.vars_names(0)