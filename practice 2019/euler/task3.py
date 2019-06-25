import math


def task3(number):
  def isPrime(n):
    if n % 2 == 0:
      return n == 2
    d = 3
    while d * d <= n and n % d != 0:
      d += 2
    return d * d > n

  c = int(math.sqrt(number))
  while (number % c != 0 or not isPrime(c)):
    c -= 1

  print(c)


task3(600851475143)
