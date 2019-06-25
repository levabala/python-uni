def fun(multiples, border):
  return sum([n if any(map(lambda s: n % s == 0, multiples)) else 0 for n in range(border)])


print(fun([3, 5], 1000))
