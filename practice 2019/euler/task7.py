def task7():
  def eratosthenes(n):
    sieve = list(range(n + 1))
    sieve[1] = 0
    for i in sieve:
      if i > 1:
        for j in range(i + i, len(sieve), i):
          sieve[j] = 0

    return list(filter(lambda b: b != 0, sieve))

  s = eratosthenes(1000000)
  n = s[10000]

  print(n)


task7()
