import time
import math
factorialsBuffer = [1]


def fact(num):
  if len(factorialsBuffer) < num:
    val = fact(num - 1) * num
    factorialsBuffer.append(val)
    return val
  return factorialsBuffer[num - 1]


def calcE(to, power=1):
  a = 1
  e = 1
  while to > 0:
    e += (power ** a) / fact(a)
    a += 1
    to -= 1
  return e


def calcSin(x, eps=0.0001):
  a = 3
  s = x
  b = -1
  add = x
  while abs(add) > eps:
    add = b * (x ** a) / fact(a)
    s += add
    a += 2
    b *= -1
  return s


def felem(i):
  if i == 0:
    return 1
  return 1 / fact(i)


def sumR(f, n):
  return sum([f(i) for i in range(n)])


def sumRP(f, n, pred):
  val = f(n)
  sum = 0
  while pred(val):
    sum += val
    val = f(n)
  return sum


def pred(x):
  return abs(x) < 0.1 ** 3


def fpi(i):
  return 4 * 1 / (i + 1) * (-1 if i % 2 == 1 else 1)


def fsin(x):
  return lambda k: ((-1) ** k) * (x ** (2 * k + 1)) / (fact(2 * k + 1))


x = math.pi / 2
r1 = sumR(fsin(x), 3)
r2 = sumR(fsin(x), 10)
r3 = sumR(fsin(x), 30)

print(r1)
print(r2)
print(r3)
