from sorts.sortInfo import SortInfo


def bubbleSort(arr, progress=lambda x: x):
  swaps = 0
  compares = 0

  n = len(arr)
  for i in range(n):
    for j in range(0, n-i-1):
      if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = arr[j+1], arr[j]
        swaps += 2

      compares += 1

    progress(i / n)

  return SortInfo(swaps=swaps, compares=compares)
