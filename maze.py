import sys
import os
import time
import math
from random import random
from functools import reduce

terminalHeight, terminalWidth = os.popen('stty size', 'r').read().split()

terminalWidth = int(terminalWidth)
terminalHeight = int(terminalHeight)

os.system('clear')
sys.setrecursionlimit(1500)


def generateRandomMaze(width, height, density):
  startX = 2
  startY = math.floor(height / 2)

  endX = width - 2
  endY = startY

  maze = []
  for y in range(height):
    row = []
    maze.append(row)
    for x in range(width):
      row.append(1 if random() < density else 0)

  maze[startY][startX] = 2
  maze[endY][endX] = 3

  return maze


def moveUpCursor(count, force=False):
  while count:
    sys.stdout.write("\033[F")  # Cursor up one line
    if force:
      sys.stdout.write("\033[K")  # Clear to the end of line
    count -= 1


2


def parseMaze(s):
  maze = []
  rows = list(filter(lambda r: len(r) != 0, s.split('\n')))
  for y in range(len(rows)):
    items = list(map(lambda i: int(i), rows[y].strip().split(' ')))
    maze.append(items)

  return maze


def getPath(maze, ids, doPrint=False):
  deltas = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

  def getStartCoord(maze):
    for y in range(len(maze)):
      for x in range(len(maze[y])):
        if ids[maze[y][x]] == 'start':
          return (x, y)
    return None

  def getEndCoord(maze):
    for y in range(len(maze)):
      for x in range(len(maze[y])):
        if ids[maze[y][x]] == 'end':
          return (x, y)
    return None

  def getAround(heights, x, y):
    def getHeight(pos):
      x = pos[0]
      y = pos[1]

      width = len(heights[0])
      height = len(heights)
      if x < 0 or x >= width or y < 0 or y >= height:
        return None

      return heights[y][x]

    positions = list(map(lambda delta: (x + delta[0], y + delta[1]), deltas))
    around = list(map(getHeight, positions))

    return around

  checkedPositions = {}
  global hasPrinted, iteration
  hasPrinted = False
  iteration = 0

  def getWalkNextIterator(heigths, x, y, tx, ty, offsetX=0, offsetY=0, steps=0):
    if x == tx and y == ty:
      return True

    around = list(map(lambda h: -2 if h == None else h, getAround(heights, x, y)))

    unknownExists = any(map(lambda h: h == 0, around))
    if not unknownExists:
      return lambda: False

    directions = list(filter(lambda value: value != -1,
                             map(lambda data: data[0] if data[1] == 0 else -1, enumerate(around))))

    def generateIteratorGenerator(pos):
      x = pos[0]
      y = pos[1]

      dist = steps + 2
      heights[y][x] = dist

      if doPrint:
        stringMap = '\n'.join(map(lambda row: ''.join(
            map(lambda i: ('-' if i == -1 else str(i)).rjust(3), row)), heights))

        global hasPrinted, iteration
        if hasPrinted:
          moveUpCursor(len(stringMap) + 1)

        print(iteration)
        print(stringMap)
        print()

        hasPrinted = True

      iteration += 1

      return lambda: getWalkNextIterator(heights, x, y, tx, ty, offsetX, offsetY, steps + 1)

    def reducer(iterators, iterator):
      if type(iterators) is bool:
        return iterators

      result = iterator()

      if type(result) is bool:
        return result

      return iterators + [result]

    def checkPosition(pos):
      x = pos[0]
      y = pos[1]

      if x in checkedPositions and y in checkedPositions[x]:
        return False

      if not x in checkedPositions:
        checkedPositions[x] = []

      checkedPositions[x].append(y)

      return True

    def directionToPos(direction):
      delta = deltas[direction]

      nx = x + delta[0]
      ny = y + delta[1]

      return (nx, ny)

    iteratorGenerators = list(map(generateIteratorGenerator, list(
        filter(checkPosition, map(directionToPos, directions)))))
    return lambda: reduce(reducer, iteratorGenerators, [])

  hMap = {
      'wall': -1,
      None: 0,
      'start': 1,
      'end': 0
  }

  heights = list(map(lambda row: list(
      map(lambda item: hMap[ids[item]], row)), maze))

  startCoord = getStartCoord(maze)
  endCoord = getEndCoord(maze)

  sx = startCoord[0]
  sy = startCoord[1]
  tx = endCoord[0]
  ty = endCoord[1]

  def downhill(heights, path=[endCoord]):
    lastPosition = path[-1]

    if lastPosition[0] == startCoord[0] and lastPosition[1] == startCoord[1]:
      return path

    around = list(map(lambda val: math.inf if val == None or val < 1 else val, getAround(
        heights, lastPosition[0], lastPosition[1])))

    minHeight = min(around)

    direction = around.index(minHeight)
    delta = deltas[direction]

    newPosition = (lastPosition[0] + delta[0], lastPosition[1] + delta[1])
    path.append(newPosition)

    return downhill(heights, path)

  def resolveIterators(iterator, initializer=True):
    currentValue = iterator

    if type(currentValue) is bool:
      return currentValue

    if initializer:
      def transformer(v): return v if type(v) == list else [v]

      def reducer(iteratons): return list(filter(lambda v: v != False, reduce(
          lambda acc,
          iterator: acc + transformer(iterator()), iteratons, []
      )))

      firstIterations = reducer(currentValue)

      iterations = firstIterations
      while (len(iterations)):
        pathFound = any(map(lambda value: value == True, iterations))

        if pathFound:
          return True

        iterations = reducer(iterations)

      return False

    newIterators = list(
        map(lambda iteratorGenerator: iteratorGenerator(), currentValue))

    return newIterators

  pathExists = resolveIterators(getWalkNextIterator(heights, sx, sy, tx, ty)())
  if not pathExists:
    return []

  path = downhill(heights)

  if doPrint:
    heightsCopy = list(
        map(lambda row: list(map(lambda value: 'O' if value == -1 else value, row)), heights))
    for coord in path:
      heightsCopy[coord[1]][coord[0]] = '*'

    heightsCopy[startCoord[1]][startCoord[0]] = 'S'
    heightsCopy[endCoord[1]][endCoord[0]] = 'E'

    heightsCopy = list(
        map(lambda row: list(map(lambda value: ' ' if type(value) == int else value, row)), heightsCopy))

    moveUpCursor(len(heightsCopy) + 2)

    print('\n'.join(map(lambda row: ''.join(map(lambda i: str(i).rjust(3), row)), heightsCopy)))
    sys.stdout.write("\033[K")
    print()
    print('path length: {}'.format(len(path)))

  return path


maze1 = '''
  0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 1 0 3 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 1 0 0 0 0 0
  0 0 0 1 0 0 0 1 0 1 0 0 0 1 1 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0
  0 0 0 1 0 0 0 1 0 0 0 1 0 0 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0
  0 0 0 1 0 1 0 1 0 1 0 1 0 0 0 0 0 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 0 1 0
  0 1 0 1 0 1 0 1 0 1 0 1 0 1 1 0 1 1 1 0 1 0 0 0 0 0 0 0 0 0 1 0 0 1 1 1 1 1 0
  0 1 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 1 1 1 0 0 0
  2 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 1 0 0 1 0 0 1 1 1 1 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
'''

maze2 = '''
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 3 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
'''

maze3 = '''
  0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0
  0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 1 1 1 1 1 0 0 1 0 0 0 0 0 0 0 1 0
  0 0 1 0 1 0 0 1 0 1 0 0 1 1 1 1 1 0 1 0 1 0 0 0 0 0 1 0 0 1 0 1 1 1 1 1 0 0 0
  0 0 1 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 1 0 0 0 0 0 1 0 0 0
  0 0 1 0 0 0 0 1 0 0 1 0 0 0 1 0 0 1 1 1 1 1 0 0 0 0 1 0 0 1 0 0 0 0 0 1 0 0 0
  0 2 1 0 0 0 0 0 0 0 0 1 0 0 1 0 1 0 0 0 0 0 1 0 0 0 1 0 0 1 1 1 1 0 0 1 3 0 0
  0 0 0 0 1 1 1 1 1 1 1 1 0 0 1 0 1 0 0 0 0 0 0 1 0 0 1 1 0 0 0 0 1 0 0 1 1 1 1
  0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 1 1 1 1 1 0 1 0 0 0 1 1 0 0 0 1 0 1 1 0 0 0
  0 0 0 0 0 0 1 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 0 1 0 0 0 0 1 1 0 0 1 0 1 0 0 0 0
  0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 1 1 1 1 0 0 0 0 1 0 0 1 0 1 0 0 0 0
  0 0 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
'''

ids = {
    0: None,
    1: 'wall',
    2: 'start',
    3: 'end'
}

# parsedMaze = parseMaze(maze3)
parsedMaze = generateRandomMaze(30, 20, 0.3)

if (len(parsedMaze[0]) * 3 < terminalWidth or len(parsedMaze) < terminalHeight):
  getPath(parsedMaze, ids, doPrint=True)

print('calculations with no printing...')

startTime = time.time()
path = getPath(parsedMaze, ids, doPrint=False)
endTime = time.time()

moveUpCursor(1, True)

print('', end='\r')

if not path:
  print('no path exists!')
print('time elapsed (real): {}ms'.format((endTime - startTime)))
