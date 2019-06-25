import math


def task4():
  def isPalindrome(number):
    digits = math.ceil(math.log10(number))
    if digits % 2 != 0:
      return False

    s = str(number)
    h = digits // 2
    left = s[:h]
    right = s[h:][::-1]

    return left == right

  biggest = 0
  for n1 in range(999, 99, -1):
    for n2 in range(999, 99, -1):
      n = n1 * n2

      if isPalindrome(n) and n > biggest:
        biggest = n

  print(biggest)


task4()
