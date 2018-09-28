def cubrt(t, p, eps, r=None, lastDiff=0):
  if r == None or lastDiff == None:
    r = t
  newRoot = ((p - 1) / p) * r + (t / (r ** (p - 1) * p))
  diff = abs(t - newRoot ** 2)
  print("diff: " + str(diff))
  if diff <= eps or diff == lastDiff:
    return newRoot
  return cubrt(t, p, eps, newRoot, diff)


eps = 0.1
res = cubrt(8, 3, eps)
print(res)
