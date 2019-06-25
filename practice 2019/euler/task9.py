import math


def task9():
  for a in range(1000, 1, -1):
    for b in range(1000, 1, -1):
      c = math.sqrt(a ** 2 + b ** 2)
      if a + b + c == 1000:
        print(a, b, c)
        print(a * b * c)
        return


task9()
