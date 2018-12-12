from sorts.sortInfo import SortInfo


def shellSort(arr):
  swaps = 0
  compares = 0

  n = len(arr)
  gap = n//2

  compares += 1
  while gap > 0:
    for i in range(gap, n):
      temp = arr[i]
      j = i

      while True:
        compares += 1
        if not j >= gap:
          break

        compares += 1
        if not arr[j-gap] > temp:
          break

        arr[j] = arr[j-gap]
        j -= gap
        swaps += 1

      arr[j] = temp
      swaps += 1

    gap //= 2
    compares += 1

  return SortInfo(swaps=swaps, compares=compares)
