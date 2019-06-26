from math import tanh
from random import random


def process(input, hidden):
  output = sum(map(lambda v: tanh(input * v), hidden))
  res = output >= 0

  return res


def mutate(hidden, maxDelta=0.1):
  return list(map(lambda v: v + (random() - 0.5) * maxDelta, hidden))


def hidden(count=3):
  return list(map(lambda v: (random() - 0.5) * 2, range(count)))
