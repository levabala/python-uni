class Account:
  def __init__(self):
    self.__rest = 0

  def deposit(self, amount):
    self.__rest += amount


acc = Account()
acc.deposit(140)

print(acc.rest)
