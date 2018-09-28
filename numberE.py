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


eps = 1 / (10 ** 40)
print("eps: " + str(eps))
power = math.pi
tries = 4

times = []
result = 0
for x in range(tries):
  s1 = time.time()
  result = calcSin(power, eps)
  s2 = time.time()
  d1 = s2 - s1
  times.append(d1)
  print("time#{0}: {1}".format(x, d1))
print("res: " + str(result))
