from sorts.sortInfo import SortInfo


def quickSort(array, progress=lambda x: x):
  info = [0, 0]
  newArr = _sort(array, info, len(array), progress)
  for i in range(len(array)):
    array[i] = newArr[i]

  return SortInfo(swaps=info[0], compares=info[1])


def _sort(array, sortInfo, initLength, progress):
  swaps = 0
  compares = 0

  less = []
  equal = []
  greater = []

  compares += 1
  if len(array) > 1:
    progress(1 - len(array) / initLength)

    pivot = array[0]

    for x in array:
      if x < pivot:
        less.append(x)
        swaps += 1
      if x == pivot:
        equal.append(x)
        swaps += 1
      if x > pivot:
        greater.append(x)
        swaps += 1

      compares += 3

    sortInfo[0] += swaps
    sortInfo[1] += compares

    return _sort(less, sortInfo, initLength, progress)+equal+_sort(greater, sortInfo, initLength, progress)
  else:
    return array


if __name__ == '__main__':
  a = [1, 2, 3, 4, 5]
  info = quickSort(a)
  print(a)
  print(info)
