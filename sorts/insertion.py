from sorts.sortInfo import SortInfo


def insertionSort(data, progress=lambda x: x):
  swaps = 0
  compares = 0

  for i in range(len(data)):
    j = i - 1
    key = data[i]

    while True:
      compares += 1
      if not data[j] > key:
        break

      compares += 1
      if not j >= 0:
        break

      data[j + 1] = data[j]
      j -= 1
      swaps += 1

    data[j + 1] = key
    swaps += 1

    progress(i / len(data))

  return SortInfo(swaps=swaps, compares=compares)


if __name__ == '__main__':
  a = [1, 2, 3, 4, 5]
  info = insertionSort(a)
  print(a)
  print(info)
