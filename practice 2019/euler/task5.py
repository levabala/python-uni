def task5():
  def check(num):
    for i in range(1, 21):
      if num % i != 0:
        return False

    return True

  c = 1
  while (not check(c)):
    c += 1
    if c % 100000 == 0:
      print(c)

  print("result: {0}".format(c))


task5()
