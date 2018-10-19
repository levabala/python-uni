def searchNearestLeftIndex(arr, value):
  i = 0
  r = len(arr)

  while r > 1:
    if arr[i] > value:
      i = i // 2
    else:
      i += r // 2
    r = r // 2

  return i


def sortNode(arr):
  for i in range(len(arr)):


def sortInsert(arr):
  def insertToLeft(arr, val, startIndex):
    i = startIndex
    while i > 0 and val < arr[i - 1]:
      arr[i] = arr[i - 1]
      i -= 1
    arr[i] = val

  for i in range(1, len(arr)):
    if arr[i] < arr[i - 1]:
      insertToLeft(arr, arr[i], i)


def sortBubble(arr):
  def iterateSort(arr):
    ss = True
    for i in range(len(arr) - 1):
      if arr[i] > arr[i + 1]:
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
        ss = False
    return ss

  while not iterateSort(arr):
    pass


res = [1, 3, 2, 5, 4, 4, 4, 9, 9, 10, 5, 99, 0]

sortInsert(res)

print(res)
