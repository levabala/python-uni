def task6():
  r = range(1, 101)
  c1 = sum(map(lambda n: n ** 2, r))
  c2 = sum(r) ** 2

  d = c2 - c1
  print(d)


task6()
