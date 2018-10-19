import math


def findSolve(fun, eps=0.000001, a=1, b=3.1, it=100):
  if it <= 0:
    return "max deep reached"

  x = (a + b) / 2

  string = "{0:.5g} {0:.5g} {0:.5g} {0:.5g}"
  print(string.format(a, b, x, fun(x)))

  if abs(fun(x)) < eps:
    return b

  if fun(a) * fun(x) > 0:
    a = x
  else:
    b = x
  return findSolve(fun, eps, a, b, it - 1)


def ff(x):
  return math.sin(x) - x / 2


def ff2(x):
  return x ** 3 - 3

x = findSolve(ff)
print(x)
