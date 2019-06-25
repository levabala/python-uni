import math
from collections import namedtuple

# I: 1 pack per month
# II: 2 packs per month
# III: I scenario + at 6th you pay 10% of start money credit

Scenarious = namedtuple(
    "Scenarious", "name moneyCredit month percentPerYear moneyToPayTotal moneyToPayPeriod moneyToPayPerPeriod, periodsCount moneyDiff")


# def calcMonthCoeff(percentPerYear, years):
#   return (((percentPerYear * 100) ** (1/12) ** (1/years)) / 100)

def calcMonthCoeff(percentPerYear, monthes):
  i = percentPerYear / 12
  return i * ((1 + i) ** monthes) / ((1 + i) ** monthes - 1)


def calcFirstScenarious(money, monthes, percentPerYear):
  moneyPerMonth = money * calcMonthCoeff(percentPerYear, monthes)
  moneyPaid = moneyPerMonth * monthes
  return Scenarious("I Scenarious", money, monthes, percentPerYear, moneyPaid, "1 month", moneyPerMonth, monthes, moneyPaid - money)


def calcSecondScenarious(money, monthes, percentPerYear, paymentCoeff=1):
  moneyToPayLeft = money
  monthesDone = 0
  moneyPaid = 0
  moneyPerMonthToPay = money * calcMonthCoeff(percentPerYear, monthes) * paymentCoeff

  while (moneyToPayLeft > 0):
    moneyToPayLeft *= 1 + percentPerYear / 12
    toPay = min(moneyPerMonthToPay, moneyToPayLeft)

    moneyPaid += toPay
    moneyToPayLeft -= toPay
    monthesDone += 1

  return Scenarious("ororororp Scenarious", money, monthes, percentPerYear, moneyPaid, "1 month", "unknown", monthesDone, moneyPaid - money)


def calcThirdScenarious(money, monthes, percentPerYear):
  moneyToPayLeft = money
  monthesDone = 0
  moneyPaid = 0
  moneyPerMonthToPay = money * calcMonthCoeff(percentPerYear, monthes) * 2

  while (moneyToPayLeft > 0):
    moneyToPayLeft *= 1 + percentPerYear / 12

    bigPaymentAmount = money * 0.1 if monthesDone == 6 else 0

    toPay = min(moneyPerMonthToPay + bigPaymentAmount, moneyToPayLeft)

    moneyPaid += toPay
    moneyToPayLeft -= toPay
    monthesDone += 1

  return Scenarious("Basdgsd Scenarious", money, monthes, percentPerYear, moneyPaid, "1 month", "unknown", monthesDone, moneyPaid - money)


def calcFourthScenarious(money, monthes, percentPerYear, inflation=0.04):
  moneyToPayLeft = money
  monthesDone = 0
  moneyPaid = 0
  moneyPerMonthToPay = money * calcMonthCoeff(percentPerYear, monthes) * 2

  while (moneyToPayLeft > 0):
    moneyToPayLeft *= 1 + percentPerYear / 12

    bigPaymentAmount = money * 0.1 if monthesDone == 6 else 0

    toPay = min(moneyPerMonthToPay + bigPaymentAmount, moneyToPayLeft)

    moneyPaid += toPay
    moneyToPayLeft -= toPay
    monthesDone += 1

    inflation = inflation / 12

    moneyPaid *= 1 - inflation
    moneyToPayLeft *= 1 - inflation

  return Scenarious("Basdgsd Scenarious", money, monthes, percentPerYear, moneyPaid, "1 month", "unknown", monthesDone, moneyPaid - money)


def printScenarious(s):
  for name, value in s._asdict().items():
    print("{0}: {1}".format(name, value))


# firstScenarious = calcFirstScenarious(1000000, 120, 0.1)
# secondScenarious = calcSecondScenarious(1000000, 120, 0.1, 2)
# thirdScenarious = calcThirdScenarious(1000000, 120, 0.1)
forthScenarious = calcFourthScenarious(1000000, 120, 0.1, 0.04)

# printScenarious(firstScenarious)
# printScenarious(secondScenarious)
# printScenarious(thirdScenarious)
printScenarious(forthScenarious)
