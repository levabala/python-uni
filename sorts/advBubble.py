from sorts.sortInfo import SortInfo


def advBubbleSort(a):
  swaps = 0
  compares = 0

  for i in range(len(a)-1):
    q = False

    for i in range(len(a)-1-i):
      if a[i] > a[i+1]:
        a[i], a[i+1] = a[i+1], a[i]
        swaps += 1

        q = True

      compares += 1
    if not q:
      break

  return SortInfo(swaps=swaps, compares=compares)
