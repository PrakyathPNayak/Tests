def rec(l1, l2):
    return l1[0] + l2[0] + (rec(l1[1:], l2[1:]) if len(l1) > 1 else 0)


print(rec([1, 2, 3], [4, 5, 6]))
x = lambda a, b: a[0] + b[0] + (x(a[1:], b[1:]) if len(a) > 1 else 0)
print(x([1, 2, 3], [4, 5, 6]))
