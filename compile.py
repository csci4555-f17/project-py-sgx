import argparse
import os
from libs.termcolor import colored

from compiler.ast import Module, Name, Const
from flatten import flatten
from explicate_ast import IfStmt, Eq, NEq, Is, Box, UnBox, GetTag
from desugar import desugar
from abi import set_abi
from compiler import parse
from instructions import *
from interference import interference
from graph import Uncolorable
from allocator import allocate
from benchmark import BenchMark

DEBUG = False
BENCH = False


def _dbg(title, msg=""):
    # type: (str, object) -> ()
    if DEBUG:
        print
        print colored("[DEBUG] " + title, "blue")
        if msg:
            print msg


bench_marks = {}


def _start_bm(name):
    # type: (str) -> ()
    if BENCH:
        assert name not in bench_marks, name
        mark = BenchMark(name)
        mark.start()
        bench_marks[name] = mark


def _end_bm(name):
    # type: (str) -> ()
    if BENCH:
        assert name in bench_marks, name
        mark = bench_marks[name]
        mark.stop()
        print colored(mark.result(), "yellow")
        del bench_marks[name]


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
            raise Exception(
                "Both input_code and input_filename are None! Specify one!")

        self.x86IR = []

        _start_bm("parsing")
        self.ast = parse(input_code)
        _end_bm("parsing")
        _dbg("Original AST:", self.ast)

        _start_bm("desugaring")
        self.desugared_ast = desugar(self.ast)
        _end_bm("desugaring")
        _dbg("Desugared AST:", self.desugared_ast)

        _start_bm("flattening")
        self.flat_ast = flatten(self.desugared_ast)
        _end_bm("flattening")
        _dbg("Flattened AST:", self.flat_ast)

        # enumerate vars
        self.vars = dict()  # offset from %ebp for variable address on stack
        self.bytes_used = 0
        self.colors = list(regs)

    @staticmethod
    def _expr_to_x86IR(expr, target=None):
        # type: (compiler.ast.Node, str) -> ([x86instruction])
        '''
        Compiles expr into x86IR, which puts result of expression into target.
        The target is a variable name.
        '''
        x86IR = []
        if isinstance(expr, compiler.ast.Add):
            x86IR.append(addl(expr.left, expr.right))
            if target is not None and target != expr.right:
                x86IR.append(movl(expr.right, target))
        elif isinstance(expr, compiler.ast.UnarySub):
            if target is not None and expr.expr != target:
                x86IR.append(movl(expr.expr, target))
                x86IR.append(negl(target))
        elif isinstance(expr, compiler.ast.CallFunc):
            pad_instr = pad_args(len(expr.args) * 4)
            x86IR.append(pad_instr)
            for name in reversed(expr.args):
                x86IR.append(pushl(name))
            x86IR.append(call(expr.node.name))
            x86IR.append(addl(Const(len(expr.args) * 4), "%esp"))
            x86IR.append(unpad_args(pad_instr))
            if target is not None and expr != target:
                x86IR.append(movl("%eax", target))
            # TODO: handle args, star args, double star args
        elif isinstance(expr, compiler.ast.Const) or isinstance(expr,
                                                                compiler.ast.Name):
            if target is not None and expr != target:
                x86IR.append(movl(expr, target))
        elif isinstance(expr, Eq):
            x86IR.append(cmpl(expr.left, expr.right))
            x86IR.append(sete_cl())
            if target is not None:
                x86IR.append(movzbl_cl(target))
        elif isinstance(expr, NEq):
            x86IR.append(cmpl(expr.left, expr.right))
            x86IR.append(setne_cl())
            if target is not None:
                x86IR.append(movzbl_cl(target))
        elif isinstance(expr, Is):
            x86IR.append(cmpl(expr.left, expr.right))
            x86IR.append(sete_cl())
            if target is not None:
                x86IR.append(movzbl_cl(target))
        elif isinstance(expr, GetTag):
            if target is not None:
                x86IR.append(movl(expr.arg, target))
                x86IR.append(andl("$3", target))
        elif isinstance(expr, Box):
            if target is not None:
                x86IR.append(movl(expr.arg, target))
                if expr.type == "int":
                    x86IR.append(sall("$2", target))
                elif expr.type == "bool":
                    x86IR.append(sall("$2", target))
                    x86IR.append(orl("$1", target))
                elif expr.type == "big":
                    x86IR.append(orl("$3", target))
                else:
                    raise TypeError(expr.type)
        elif isinstance(expr, UnBox):
            if target is not None:
                x86IR.append(movl(expr.arg, target))
                if expr.type == "small":
                    x86IR.append(sarl("$2", target))
                elif expr.type == "big":
                    x86IR.append(andl("$0xfffffffc", target))
                else:
                    raise TypeError(expr.type)
        else:
            raise TypeError(expr)
        return x86IR

    def _get_x86IR(self):
        def __get_x86IR(nodes):
            # type: ([compiler.ast.Node]) -> ([x86instruction])
            x86IR = []
            for stmt in nodes:
                if isinstance(stmt, compiler.ast.Printnl):
                    if len(stmt.nodes) > 1:
                        return NotImplemented("Cannot print to multiple nodes")
                    if len(stmt.nodes) < 1:
                        return NotImplemented(
                            "Cannot print zero nodes. TODO: print endl")
                    node = stmt.nodes[0]
                    pad_instr = pad_args(4)
                    x86IR.append(pad_instr)
                    x86IR.append(pushl(node))
                    x86IR.append(call("print_any"))
                    x86IR.append(addl(Const(4), "%esp"))
                    x86IR.append(unpad_args(pad_instr))
                elif isinstance(stmt, compiler.ast.Assign):
                    if len(stmt.nodes) > 1:
                        raise NotImplementedError(
                            "Cannot assign to multiple nodes")
                    node_0 = stmt.nodes[0]
                    x86IR += self._expr_to_x86IR(stmt.expr, node_0)
                elif isinstance(stmt, compiler.ast.Discard):
                    x86IR += self._expr_to_x86IR(stmt.expr, None)
                elif isinstance(stmt, IfStmt):
                    x86IR.append(if_instr(stmt.test,
                                          __get_x86IR(stmt.then_.nodes),
                                          __get_x86IR(stmt.else_.nodes))
                                 )
                else:
                    raise NotImplementedError("Not implemented.")
            return x86IR

        self.x86IR = __get_x86IR(self.flat_ast.node.nodes)
        return

    def _get_x86IR_liveness(self):
        def __get_x86IR_liveness(x86IR, curr_live):
            for i in range(len(x86IR) - 1, -1, -1):
                x86IR[i].live_vars_after = curr_live.copy()
                if isinstance(x86IR[i], if_instr):
                    live_then_ = __get_x86IR_liveness(x86IR[i].then_,
                                                      curr_live.copy())
                    live_else_ = __get_x86IR_liveness(x86IR[i].else_,
                                                      curr_live.copy())
                    curr_live = live_then_ | live_else_
                curr_live -= set(x86IR[i].vars_written())
                curr_live |= set(x86IR[i].vars_read())
            return curr_live

        _start_bm("liveness")
        __get_x86IR_liveness(self.x86IR, set())
        _end_bm("liveness")

    def _build_interference_graph(self):
        _start_bm("interference")
        self.interference_graph = interference(self.x86IR)
        _end_bm("interference")

    def _allocate_regs(self):
        def generate_color():
            self.bytes_used += 4
            new_color = "-" + str(self.bytes_used) + "(%ebp)"
            self.colors.append(new_color)
            return new_color

        _start_bm("coloring")
        self.interference_graph.color(self.colors, generate_color)
        self.vars = {name: node.color for name, node in
                     self.interference_graph.nodes.items()}
        for instr in self.x86IR:
            instr.assign_locations(self.vars)
        _end_bm("coloring")

    def _introduce_spill(self):
        def spill(x86IR):
            spilled = False
            skip_next = False
            for i in range(len(x86IR)):
                instr = x86IR[i]
                if skip_next:
                    skip_next = False
                    continue
                if isinstance(instr, if_instr):
                    if spill(instr.then_) or spill(instr.else_):
                        spilled = True
                if instr.is_mem_to_mem():
                    var = allocate()
                    x86IR.insert(i, unspillableMovl(x86IR[i].vars[0], var))
                    x86IR[i + 1].vars[0] = var
                    spilled = True
                    skip_next = True
            return spilled

        _start_bm("spilling")
        spilled = spill(self.x86IR)
        _end_bm("spilling")
        return spilled

    def _update_padding(self):
        def __update_padding(x86IR):
            for instr in x86IR:
                if isinstance(instr, pad_args):
                    # 8 is added here since we need to account for the initial push %ebp in
                    # the prologue (4) + the space saved for the return address (4), on top
                    # of the space allocated for locals
                    instr.calc_padding(self.bytes_used + 8)
                    instr.assign_locations(self.vars)
                if isinstance(instr, if_instr):
                    __update_padding(instr.then_)
                    __update_padding(instr.else_)
                if isinstance(instr, unpad_args):
                    instr.assign_locations(self.vars)

        __update_padding(self.x86IR)

    def _rm_nops(self):
        # We must go through the list in reverse since we are removing items.
        def __rm_nops(x86IR):
            for i, instr in reversed(list(enumerate(x86IR))):
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
                        del x86IR[i]
                elif isinstance(instr, pad_args):
                    if instr.padding == 0:
                        del x86IR[i]
                elif isinstance(instr, unpad_args):
                    if instr.pad_instr.padding == 0:
                        del x86IR[i]
                elif isinstance(instr, IfStmt):
                    __rm_nops(instr.then_)
                    __rm_nops(instr.else_)
                elif isinstance(instr, addl):
                    if instr.vars[0] == Const(0):
                        del x86IR[i]

        __rm_nops(self.x86IR)

    def _compile_prologue(self):
        # type: () -> str
        main = abi.label("main")
        return ".globl " + main + "\n" + main + ":\npushl %ebp\nmovl %esp, %ebp\nsubl $" + str(
            self.bytes_used) + ", %esp\n\n"

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
        _dbg("Graph Coloring", self.interference_graph.nodes.values())
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
    parser.add_argument('-d', '--debug', dest='debug', action='store_true')
    parser.add_argument('-b', '--bench', dest='bench', action='store_true')
    parser.add_argument('-t', '--target',
                        help="The target platform to compile for ('mac' or 'linux')",
                        type=str)
    args = parser.parse_args()

    global DEBUG
    DEBUG = args.debug
    global BENCH
    BENCH = args.bench
    if args.target is not None:
        set_abi(args.target)
    pc = _ProgramCompiler(input_filename=args.input_file)
    with open(os.path.splitext(args.input_file)[0] + ".s", 'wb') as outfile:
        pc.compile_to_file(outfile)


if __name__ == "__main__":
    main()
