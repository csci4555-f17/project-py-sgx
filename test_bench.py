#!/usr/bin/env python
from compile import _ProgramCompiler
import subprocess
import os
from shutil import rmtree as rm
import traceback

from libs.termcolor import colored


class TestCompiler(object):
	def __init__(self, input_code=None, input_filename=None, subprocess_stdin=None, test_name=None, build_dir="./benchmarks/target"):
		# type: (str, str, list) -> None
		# if input_filename is provided, input_code is ignored

		rm(build_dir, ignore_errors=True)
		os.mkdir(build_dir)

		self.build_dir = build_dir
		if input_filename is not None:
			self.source_filename = input_filename
		elif input_code is not None:
			self.source_filename = build_dir + "/.tmp_test.py"
			with open(self.source_filename, "w") as source_file:
				source_file.write(input_code)
		else:
			raise Exception("Both input_code and input_filename are None! Specify one!")

		if subprocess_stdin is not None:
			self.subprocess_stdin = subprocess_stdin

		if test_name is not None:
			self.test_name = test_name
		else:
			self.test_name = ""

		self.assembly_filename = build_dir + "/.tmp_test.s"
		self.binary_filename = build_dir + "/.tmp_test"

	def _compile_python(self):
		assembly_file = open(self.assembly_filename, 'wb')
		p = _ProgramCompiler(input_filename=self.source_filename)
		p.compile_to_file(assembly_file)
		print("bytes used", p.bytes_used)

	def _compile_assembly(self):
		gcc_proc = subprocess.Popen(['gcc', '-m32', '-g', '-lm', self.assembly_filename,
									 'runtime/libpyyruntime.a', '-o', self.binary_filename],
									stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		build_out, build_err = gcc_proc.communicate()

		if gcc_proc.returncode != 0:
			raise Exception("Compilation failed!\n" + build_out + "\n" + build_err)

	@staticmethod
	def empty_file(filename):
		# open/create a file and delete its content
		f = open(filename, 'wb', os.O_CREAT)
		f.seek(0)
		f.truncate()
		f.close()

	def _run_binary(self):
		proc = subprocess.Popen([self.binary_filename],
								stdout=subprocess.PIPE,
								stdin=subprocess.PIPE)
		if hasattr(self, 'subprocess_stdin'):
			for inp in self.subprocess_stdin:
				proc.stdin.write(inp + "\n")

		self.binary_out, self.binary_err = proc.communicate()
		self.binary_ret = proc.returncode

	def Run(self):
		class MissMatchException(RuntimeWarning):
			pass

		self.empty_file(self.binary_filename)
		self.empty_file(self.assembly_filename)

		try:
			self._compile_python()
			self._compile_assembly()
			self._run_binary()

			if hasattr(self, 'binary_out'):
				print "> Binary output:"
				print self.binary_out
		except Exception as e:
			print colored(">> TEST FAILED ", "red"), self.test_name
			print e
			if not isinstance(e, MissMatchException):
				traceback.print_exc()

			if hasattr(self, 'binary_out'):
				print "> Binary output:"
				print self.binary_out

			print

		finally:
			pass
			#rm(self.build_dir, ignore_errors=True)

def main():
	test_dir = "./benchmarks/"
	for test_filename in sorted(os.listdir(test_dir)):
		if test_filename.endswith("e.py"):
			try:
				with open(test_dir + test_filename, 'r') as test_file:
					input_code = test_file.read()
			except IOError:
				print('Could not open ' + test_filename)
				continue

			subprocess_stdin = None
			try:
				with open(test_dir + test_filename[:-3] + ".in", 'r') as test_inputfile:
					subprocess_stdin = test_inputfile.read().splitlines()
			except IOError:
				pass

			TestCompiler(input_code=input_code, subprocess_stdin=subprocess_stdin, test_name=test_filename).Run()
	return


if __name__ == "__main__":
	main()
