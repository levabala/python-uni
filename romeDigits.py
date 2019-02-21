def mult(x, n):

  if x == 0 or n == 0:
    return 0

  if n % 2 == 0:
    return twice(mult(x, n / 2))

  return x + mult(x, n - 1)


def twice(x):
  return x + x


a = mult(60, 345)
print(a)
