# libs
from random import randint
from statistics import mean
from sorts.sortInfo import SortInfo

# sorts
from sorts.bubble import bubbleSort
from sorts.advBubble import advBubbleSort
from sorts.insertion import insertionSort
from sorts.shell import shellSort

SORTS = [bubbleSort, advBubbleSort, insertionSort, shellSort]

TEST_LENGTHS = [10 ** 1, 10 ** 2, 10 ** 3]  # , 10 ** 4]  # , 10 ** 5]
APPROXIMATE_ITERATIONS = 3
RANDOM_RANGE = (-10 ** 5, 10 ** 5)

# global object for storing analyzing results
analyzeData = []


# test different lengths
for i in range(len(TEST_LENGTHS)):
  length = TEST_LENGTHS[i]
  analyzeData.append([])

  data = [[] for i in range(len(SORTS))]  # sorts index : array of info

  # do sorting several times to get more realistic info
  for i2 in range(APPROXIMATE_ITERATIONS):

    # generate random 1d array
    testArray = [randint(*RANDOM_RANGE) for i in range(length)]

    # iterate over target sort types
    for i3 in range(len(SORTS)):
      sortFunc = SORTS[i3]
      # array for storing info'bout sort params (swaps and compares count)

      # copy array to sort (we mustn't change target array)
      arrCopy = testArray.copy()

      # do sorting
      info = sortFunc(arrCopy)

      # register data of current sorting
      data[i3].append(info)

  for i2 in range(len(data)):
    sortData = data[i2]

    # approximate data
    allSwaps = [sortData[i].swaps for i in range(len(sortData))]
    allCompares = [sortData[i].compares for i in range(len(sortData))]

    # we use mean() to tage average value
    sortDataApprox = SortInfo(mean(allSwaps), mean(allCompares))

    analyzeData[i].append(sortDataApprox)

for i in range(len(analyzeData)):
  data = analyzeData[i]
  print('Length \033[1m{}\033[0m'.format(TEST_LENGTHS[i]))

  for i2 in range(len(SORTS)):
    print('Sort \033[92m{}\033[0m swaps: {}, compares: {}'.format(
        SORTS[i2].__name__, round(data[i2].swaps, 0), round(data[i2].compares, 0)))

  print()
