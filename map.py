import math


def map(l, processor):
  res = []
  for el in l:
    res.append(processor(el))
  return res


res = map([1, 2, 3, 4, 5, 6], math.sqrt)
print(res)
