# Proposal

### 1. Who are the members of your team?
Our team consists of Albert Dayn and Sergey Frolov.

### 2. What basic problem will your project try to solve?
We want to enable the use of secured and encrypted sections of memory directly from our subset of Python.
Intel includes SGX (Software Gaurd Extentions) in their x86-64 chipsets.
These are instructions that allow the creation of segments of memory that are encrypted until data reaches the physical processor, enabling the creation of applications that can secure data from the very operating system they are running on.
We will expose these instructions through python functions, so that programmers can create memory secured from attackers while still using a high level language.
