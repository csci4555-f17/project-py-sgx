d1 = {True: 1, 0: False, 44: -90}
d2 = {True: 1, 0: False, 44: -90}
d3 = {}
a = False
b = False
eax = -99
val1=a
val2=eax
d1[val1]= False +- b if (False +- a if b else eax) else 0
d2[val1]= 0 +- True if (((False +- a if b else eax) +- 0 if b else b) +- -99 if a else (False +- a if b else eax)) else False
d3[val1]= eax +- -99 if ((False +- a if b else eax) +- 0 if b else b) else a
d1[val2]= 0 +- (((False +- a if b else eax) +- 0 if b else b) +- -99 if a else (False +- a if b else eax)) if (False +- a if b else eax) else eax
d2[val2]= 0 +- b if (False +- a if b else eax) else -99
d3[val2]= False +- False if a else (((False +- a if b else eax) +- 0 if b else b) +- -99 if a else (False +- a if b else eax))
d3[val1] = (input() +- -99 if b else eax)
d1[val2] = ((False +- a if b else eax) +- 0 if b else b)
print d1[val1]
print d1[val2]
print d2[val1]
print d2[val2]
print d3[val1]
print d3[val2]
