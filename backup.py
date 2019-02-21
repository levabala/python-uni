import sys
import os
from functools import reduce
from math import inf

os.system('clear')
sys.setrecursionlimit(1500)


def moveUpCursor(count):
  while count:
    # sys.stdout.write("\033[K")  # Clear to the end of line
    sys.stdout.write("\033[F")  # Cursor up one line
    count -= 1


def parseMaze(s):
  maze = []
  rows = list(filter(lambda r: len(r) != 0, s.split('\n')))
  for y in range(len(rows)):
    items = list(map(lambda i: int(i), rows[y].strip().split(' ')))
    maze.append(items)

  return maze


def getPath(maze, ids):
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

      if x < 0 or x >= len(heights[0]) or y < 0 or y >= len(heights):
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
      print('got it!')
      print(str(x) + ' ' + str(y))
      print('steps: ' + str(steps))
      return lambda: True

    around = list(map(lambda h: -2 if h == None else h, getAround(heights, x, y)))

    unknownExists = any(map(lambda h: h == 0, around))
    if not unknownExists:
      return False

    directions = list(filter(lambda value: value != -1,
                             map(lambda data: data[0] if data[1] == 0 else -1, enumerate(around))))

    def generateIteratorGenerator(pos):
      x = pos[0]
      y = pos[1]

      dist = steps + 1
      heights[y][x] = dist

      stringMap = '\n'.join(map(lambda row: ''.join(map(lambda i: str(i).rjust(3), row)), heights))

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

    around = list(map(lambda val: inf if val == None or val < 1 else val, getAround(
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
    print('no path exists!')
    return

  path = downhill(heights)

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
  print()
  print('path length: {}'.format(len(path)))


maze1 = '''
  0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 1 0 0 0 0 0
  0 0 0 1 0 0 0 1 0 1 0 0 0 1 1 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0
  0 0 0 1 0 0 0 1 0 0 0 1 0 0 1 1 1 1 1 0 1 0 0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0
  0 0 0 1 0 1 0 1 0 1 0 1 0 0 0 0 0 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 0 1 0
  0 1 0 1 0 1 0 1 0 1 0 1 0 1 1 0 1 1 1 0 1 0 0 0 0 0 0 0 0 0 1 0 0 1 1 1 1 1 0
  0 1 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 1 1 1 0 0 0
  2 1 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 1 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 0 0 0 0 1 0 0 1 0 0 1 1 1 1 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0
  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
'''

ids = {
    0: None,
    1: 'wall',
    2: 'start',
    3: 'end'
}

getPath(parseMaze(maze1), ids)
