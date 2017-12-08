import argparse
import os
from sys import platform

from compiler.ast import Module, Name, Const
from flatten import flatten, VariableAllocator
from abi import ABI, set_abi
from compiler import parse
from instructions import *
from interference import interference
from graph import Uncolorable

DEBUG = False

class _ProgramCompiler:
	"""
	Compiles single instance of python AST into x86.
	"""

	def __init__(self, input_code=None, input_filename=None):
		# type: (Module) -> _ProgramCompiler
		if input_filename is not None:
			with open(input_filename) as input_file:
				input_code = input_file.read()
		elif input_code is None:
			raise Exception("Both input_code and input_filename are None! Specify one!")

		self.ast = parse(input_code)
		self.x86IR = []
		self.flat_ast = flatten(self.ast)

		# enumerate vars
		self.vars = dict()  # offset from %ebp for variable address on stack
		self.bytes_used = 0
		self.colors = list(regs)

		if DEBUG:
			print "[DEBUG] Original AST:"
			print(self.ast)
			print "[DEBUG] Flattened AST:"
			print(self.flat_ast)

	def _expr_to_x86IR(self, expr, target=None):
		# type: (compiler.ast.Node, str) -> ()
		'''
		Compiles expr into x86IR, which puts result of expression into target.
		The target is a variable name.
		'''
		if isinstance(expr, compiler.ast.Add):
			self.x86IR.append(addl(expr.left, expr.right))
			if target is not None and target != expr.right:
				self.x86IR.append(movl(expr.right, target))
		elif isinstance(expr, compiler.ast.UnarySub):
			if target is not None and expr.expr != target:
				self.x86IR.append(movl(expr.expr, target))
				self.x86IR.append(negl(target))
		elif isinstance(expr, compiler.ast.CallFunc):
			pad_instr = pad_args(0)
			self.x86IR.append(pad_instr)
			self.x86IR.append(call(expr.node.name))
			self.x86IR.append(unpad_args(pad_instr))
			if target is not None and expr != target:
				self.x86IR.append(movl("%eax", target))
			# TODO: handle args, star args, double star args
		elif isinstance(expr, compiler.ast.Const) or isinstance(expr, compiler.ast.Name):
			if target is not None and expr != target:
				self.x86IR.append(movl(expr, target))
		else:
			raise TypeError(expr)

	def _get_x86IR(self):
		# type: (compiler.ast.Node) -> ()
		for stmt in self.flat_ast.node.nodes:
			if isinstance(stmt, compiler.ast.Printnl):
				if len(stmt.nodes) > 1:
					return NotImplemented("Cannot print to multiple nodes")
				if len(stmt.nodes) < 1:
					return NotImplemented("Cannot print zero nodes. TODO: print endl")
				node = stmt.nodes[0]
				pad_instr = pad_args(4)
				self.x86IR.append(pad_instr)
				self.x86IR.append(pushl(node))
				self.x86IR.append(call("print_int_nl"))
				self.x86IR.append(unpad_args(pad_instr))
			elif isinstance(stmt, compiler.ast.Assign):
				if len(stmt.nodes) > 1:
					raise NotImplementedError("Cannot assign to multiple nodes")
				node_0 = stmt.nodes[0]
				self._expr_to_x86IR(stmt.expr, node_0)
			elif isinstance(stmt, compiler.ast.Discard):
				self._expr_to_x86IR(stmt.expr, None)
			else:
				raise NotImplementedError("Not implemented.")

	def _get_x86IR_liveness(self):
		curr_live = set()
		for i in range(len(self.x86IR) - 1, -1, -1):
			self.x86IR[i].live_vars_after = curr_live.copy()
			curr_live -= set(self.x86IR[i].vars_written())
			curr_live |= set(self.x86IR[i].vars_read())

	def _build_interference_graph(self):
		self.interference_graph = interference(self.x86IR)

	def _allocate_regs(self):
		colored = False
		while not colored:
			try:
				self.interference_graph.color(self.colors)
				colored = True
			except Uncolorable:
				self.bytes_used += 4
				self.colors.append("-" + str(self.bytes_used) + "(%ebp)")
		self.vars = {name: node.color for name, node in self.interference_graph.nodes.items()}
		for instr in self.x86IR:
			instr.assign_locations(self.vars)

	def _introduce_spill(self):
		spilled = False
		skip_next = False
		for i in range(len(self.x86IR)):
			instr = self.x86IR[i]
			if skip_next:
				skip_next = False
				continue
			if instr.is_mem_to_mem():
				var = VariableAllocator.allocate()
				self.x86IR.insert(i, unspillableMovl(self.x86IR[i].vars[0], var))
				self.x86IR[i + 1].vars[0] = var
				spilled = True
				skip_next = True
		return spilled

	def _update_padding(self):
		for instr in self.x86IR:
			if isinstance(instr, pad_args):
				# 8 is added here since we need to account for the initial push %ebp in
				# the prologue (4) + the space saved for the return address (4), on top
				# of the space allocated for locals
				instr.calc_padding(self.bytes_used + 8)
				instr.assign_locations(self.vars)
			if isinstance(instr, unpad_args):
				instr.assign_locations(self.vars)

	def _rm_nops(self):
		# We must go through the list in reverse since we are removing items.
		for i, instr in reversed(list(enumerate(self.x86IR))):
			if isinstance(instr, movl):
				v1 = instr.vars[0]
				v2 = instr.vars[1]

				loc1 = None
				if isinstance(v1, Name):
					loc1 = self.vars[v1.name]
				elif isinstance(v1, str):
					# Register
					loc1 = v1
				loc2 = None
				if isinstance(v2, Name):
					loc2 = self.vars[v2.name]
				elif isinstance(v2, str):
					# Register
					loc2 = v2

				if loc1 == loc2:
					del self.x86IR[i]
			elif isinstance(instr, pad_args):
				if instr.padding == 0:
					del self.x86IR[i]
			elif isinstance(instr, unpad_args):
				if instr.pad_instr.padding == 0:
					del self.x86IR[i]
			elif isinstance(instr, addl):
				if instr.vars[0] == Const(0):
					del self.x86IR[i]

	def _compile_prologue(self):
		# type: () -> str
		main = abi.label("main")
		return ".globl " + main + "\n" + main + ":\npushl %ebp\nmovl %esp, %ebp\nsubl $" + str(self.bytes_used) + ", %esp\n\n"

	def _get_x86(self):
		instructions = ""
		if DEBUG:
			print "[DEBUG] x86 IR"
		for instr in self.x86IR:
			x86_asm = instr.get_x86()
			if DEBUG:
				print instr, "----->", x86_asm
			instructions += x86_asm + "\n"
		return instructions

	def _compile_epilogue(self):
		# type: () -> str
		return "leave\nret\n"

	def compile(self):
		# type: () -> str
		self._get_x86IR()
		self._get_x86IR_liveness()
		self._build_interference_graph()
		self._allocate_regs()
		while self._introduce_spill():
			self._get_x86IR_liveness()
			self._build_interference_graph()
			self._allocate_regs()
		if DEBUG:
			print "[DEBUG] interference graph:"
			print self.interference_graph
		self._update_padding()
		self._rm_nops()

		asm_code = self._compile_prologue()
		asm_code += self._get_x86()
		asm_code += "movl $0, %eax\n"  # zero out return code
		asm_code += self._compile_epilogue()
		return asm_code

	def compile_to_file(self, outfile):
		# type: (file) -> None
		outfile.write(self.compile())

def main():
	parser = argparse.ArgumentParser(description='Best python compiler ever')
	parser.add_argument("input_file", help="Name of file to compile.", type=str)
	parser.add_argument('-d', '--debug', dest='DEBUG', action='store_true')
	parser.add_argument('-t', '--target', help="The target platform to compile for ('mac' or 'linux')", type=str)
	args = parser.parse_args()

	global DEBUG
	DEBUG = args.DEBUG
	if args.target is not None:
		set_abi(args.target)
	pc = _ProgramCompiler(input_filename=args.input_file)
	with open(os.path.splitext(args.input_file)[0] + ".s", 'wb') as outfile:
		pc.compile_to_file(outfile)


if __name__ == "__main__":
	main()
