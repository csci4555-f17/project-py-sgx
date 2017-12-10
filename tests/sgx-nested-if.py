testg = 0
test2 = 8
varg = 3
var2 = 5
if testg:
    testg = 1
    var1 = 3
    if testg:
        varg = var1
    else:
        var1 = varg
else:
    testg = varg
    var1 = 34 if 8 else 3
    if test2:
        var2 = 89
        varg = 98
        test2 = 8

print testg
print test2
print varg
print var1
print var2
