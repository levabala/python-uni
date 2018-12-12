from sorts.sortInfo import SortInfo


def insertionBinary(data, progress=lambda x: x):
  swaps = 0
  compares = 0

  for i in range(len(data)):
    key = data[i]
    lo, hi = 0, i - 1

    while lo < hi:
      compares += 1
      mid = lo + (hi - lo) // 2

      compares += 1
      if key < data[mid]:
        hi = mid
      else:
        lo = mid + 1

    for j in range(i, lo + 1, -1):
      data[j] = data[j - 1]
      swaps += 1

    data[lo] = key
    swaps += 1

    progress(i / len(data))

  return SortInfo(swaps=swaps, compares=compares)
