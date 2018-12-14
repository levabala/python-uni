# libs
import sys
from random import randint
from statistics import mean
from sorts.sortInfo import SortInfo
from other.bcolors import bcolors, bold, green, blue
import time


# sorts
from sorts.bubble import bubbleSort
from sorts.advBubble import advBubbleSort
from sorts.insertion import insertionSort
from sorts.insertionBin import insertionBinary
from sorts.shell import shellSort
from sorts.quicksort import quickSort

print('\n------------- SORT ALGORITHMS TESTING -------------\n')


def getTime(): return int(round(time.time() * 1000))


def main():
  SORTS = [bubbleSort, advBubbleSort, insertionSort, insertionBinary, shellSort, quickSort]
  # SORTS = [insertionSort, insertionBinary, shellSort, quickSort]
  # SORTS = [insertionBinary, shellSort, quickSort]
  # SORTS = [shellSort, quickSort]

  # TEST_LENGTHS = [int(10 ** 5), 10 ** 6, 10 ** 7]
  TEST_LENGTHS = [10 ** 2, 10 ** 3, int(10 ** 3.1)]
  # TEST_LENGTHS = [10 ** 2, 10 ** 3, int(10 ** 5)]
  # TEST_LENGTHS = [10 ** 5, 10 ** 6, int(10 ** 7)]

  APPROXIMATE_ITERATIONS = 1
  TOTAL_LENGTH = sum(TEST_LENGTHS) * APPROXIMATE_ITERATIONS * len(SORTS)
  TRIGGER_LENGTH = int(TOTAL_LENGTH / 100)
  # RANDOM_RANGE = (-10 ** 5, 10 ** 5)
  RANDOM_RANGE = (-10 ** 2, 10 ** 2)

  # global object for storing analyzing results
  analyzeData = []
  lastTriggeredLength = 0
  lengthProcessed = 0

  # test different lengths
  for i in range(len(TEST_LENGTHS)):
    length = TEST_LENGTHS[i]
    analyzeData.append([])

    print('\nstarted calculations for {}-length arrays\n'.format(length))

    data = [[] for i in range(len(SORTS))]  # sorts index : array of info

    # do sorting several times to get more realistic info
    for i2 in range(APPROXIMATE_ITERATIONS):

      # generate random 1d array
      testArray = [randint(*RANDOM_RANGE) for i in range(length)]

      # iterate over target sort types
      for i3 in range(len(SORTS)):
        timeStart = getTime()

        sortFunc = SORTS[i3]

        # copy array to sort (we mustn't change target array)
        arrCopy = testArray.copy()

        # generate progress callback
        lengthProcessedBefore = lengthProcessed

        progressInsideHappened = False

        def progressCallback(percent):
          nonlocal lastTriggeredLength
          nonlocal lengthProcessedBefore
          nonlocal sortFunc
          nonlocal timeStart
          nonlocal progressInsideHappened
          nonlocal length

          secs = (getTime() - timeStart) / 10 ** 3

          lastTriggeredLength = showProgress(
              lengthProcessedBefore + length * percent, lengthProcessedBefore, lastTriggeredLength, lengthProcessed + length, TOTAL_LENGTH, TRIGGER_LENGTH, sortFunc.__name__, secs, timeStart, progressInsideHappened, not progressInsideHappened)

          progressInsideHappened = True

        # do sorting
        info = sortFunc(arrCopy, progressCallback)

        # show progress
        lengthProcessed += length
        secs = (getTime() - timeStart) / 10 ** 3

        lastTriggeredLength = showProgress(
            lengthProcessed, lengthProcessedBefore, lastTriggeredLength, lengthProcessed, TOTAL_LENGTH, TRIGGER_LENGTH, sortFunc.__name__, secs, timeStart, True, not progressInsideHappened)

        # check if sorted correctly
        correctly = validateSorting(arrCopy)
        if not correctly:
          print('{}Wrong sorted for {} algorithm for {} elements{}'.format(
              bcolors.FAIL, sortFunc.__name__, len(testArray), bcolors.ENDC))
          input()

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

  print('\n\nR E S U L T S: \n')
  for i in range(len(analyzeData)):
    data = analyzeData[i]

    if sys.argv.__contains__('--export'):
      print('{}{:<15}{} {}{:<10}{}'.format(bcolors.OKGREEN, 'length',
                                           bcolors.ENDC, bcolors.BOLD, TEST_LENGTHS[i], bcolors.ENDC))
    else:
      print('Length {}{}{}'.format(bcolors.BOLD, TEST_LENGTHS[i], bcolors.ENDC))

    for i2 in range(len(SORTS)):
      if sys.argv.__contains__('--export'):
        print(
            '{}{:<15}{} {}{:<10}{} {}{:<10}{}'.format(
                bcolors.OKGREEN, SORTS[i2].__name__, bcolors.ENDC,
                bcolors.BOLD, int(data[i2].swaps), bcolors.ENDC,  bcolors.BOLD,
                int(data[i2].compares), bcolors.ENDC,
            ),
        )
      else:
        print(
            'Sort {}{:<15}{} swaps: {}{:<10}{} compares: {}{:<10}{} total: {}{:<10}{}'.format(
                bcolors.OKGREEN, SORTS[i2].__name__, bcolors.ENDC,
                bcolors.BOLD, int(data[i2].swaps), bcolors.ENDC,  bcolors.BOLD,
                int(data[i2].compares), bcolors.ENDC,
                bcolors.BOLD, str(int((data[i2].compares + data[i2].swaps) /
                                      TEST_LENGTHS[i] * 100)) + '%', bcolors.ENDC
            ),
        )

    print()


# function for validating if array is correctly sorted
def validateSorting(arr):
  print(blue('validating...'))
  for i in range(1, len(arr)):
    if arr[i] < arr[i - 1]:
      sys.stdout.write("\033[F")  # Cursor up one line
      sys.stdout.write("\033[K")  # Clear to the end of line
      return False

  sys.stdout.write("\033[F")  # Cursor up one line
  sys.stdout.write("\033[K")  # Clear to the end of line
  return True

# function for showing analyzing progress


def showProgress(processed, start, last, localTarget, total, trigger, processor='unknown', timeSecs=0, timeStart=0, rewrite=True, forced=False):
  diff = processed - last
  if diff > trigger or forced:
    if rewrite:
      sys.stdout.write("\033[F")  # Cursor up one line
      sys.stdout.write("\033[K")  # Clear to the end of line

    print('Progress: {}/{}% by {} ({}s, {}el/s)'.format(
        bold(int(processed / total * 100)),
        bold(int(localTarget / total * 100)),
        green(processor),
        bold('{:.3f}'.format(timeSecs)),
        bold('{:.1f}'.format(min(processed - start, localTarget -
                                 processed) / timeSecs) if timeSecs != 0 else 0)
    )
    )

    return processed

  return last


main()
