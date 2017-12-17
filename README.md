# Compiling python to a side-channel protected binary

There are numerous side-channel based attacks on protections, guaranteed by Intel SGX trusted execution. Prior research has shown that side-channels may enable a local attacker to extract information from the secure enclave. We address issues with cache, timing, and branch shadowing through a combination of known and brand new techniques to compile Python to a protected binary. We show that proposed protections efficiently eliminate side-channels.

- [Proposal](proposal.md)
- [Status Update](status-update.md)
- [Presentation](presentation.pdf)
- [Paper](paper/paper.pdf)

There is a minimal amount of starter files in this repository: a minimal run-time system for your programs, a wrapper script for your compiler `pyyc`, and a `Makefile` for your convenience.

Your compiler should take one argument for the name of the input Python `.py` file to compile, and it should produce an output x86 assembly file with the same name as the input file except that the `.py` suffix has been replaced by the `.s` suffix.

Then, to run a program compiled from your compiler. You need to do the following:

- Build the run-time system (if it is not already built).
```bash
$ make -C runtime
```
- Compile the test program.
```bash
$ ./pyyc mytests/test1.py
```
- Link your assembly with the run-time system.
```bash
$ gcc -m32 -g -lm mytests/test1.s runtime/libpyyruntime.a -o mytests/test1
```
- Run your program.
```bash
$ cat mytests/test1.in | mytests/test1 > mytests/test1.out
```

For your convenience, the `Makefile` has targets for these steps that you may use, modify, or ignore as you like.

Your compiler needs to produce code that runs on an x86 Linux machine.

Architecture:

Parse  
De-Sugar
Explicate
Flatten
Select Instructions
Allocate Regs
Update Padding
Remove Nops
Remove Structured Control Flow
Print x86
