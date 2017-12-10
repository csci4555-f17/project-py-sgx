# if 1:
#     x = 1
# else:
#     x = 2

testg = 0
varg = 3
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
print testg
print varg
print var1
