def task2():
  def fib(limit, prevPrevNum=1, prevNum=1, arr=[1]):
    n = prevNum + prevPrevNum

    if (n >= limit):
      return arr

    arr.append(n)
    return fib(limit, prevNum, n, arr)

  def even(arr):
    return list(filter(lambda l: l % 2 == 0, arr))

  return sum(even(fib(4000000)))


print(task2())
