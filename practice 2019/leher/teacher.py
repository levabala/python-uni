import operator

from leher import leher, Winner, flat
from net import hidden, mutate, process


def teach(
    receivers=[],
    dealers=[],
    roundsCount=10,
    bestSize=10,
    newSize=10,
    childPerBest=2,
    teachRound=100,
    gameIndex=0
):  
  veteran = len(receivers) + len(dealers)

  receiversMutators = list(flat(map(lambda r: map(lambda q: mutate(q), [r] * childPerBest), receivers)))
  receivers = receivers + list(map(lambda v: hidden(), range(newSize))) + receiversMutators
      
  dealersMutators = list(flat(map(lambda d: map(lambda q: mutate(q), [d] * childPerBest), dealers)))
  dealers = dealers + list(map(lambda v: hidden(), range(newSize))) + dealersMutators
      
  print("{0}, {1}".format(len(receiversMutators), len(dealersMutators)))
  print("Round {0} ({1} veteran players, {2} total)".format(gameIndex, veteran, len(receivers) + len(dealers)))

  receiversPoints = [0] * len(receivers)
  dealersPoints = [0] * len(receivers)

  # total = roundsCount * len(receivers) * len(dealers)
  done = 0
  for rr in range(roundsCount):
    for receiverIndex in range(len(receivers)):
      for dealerIndex in range(len(dealers)):
        receiver = receivers[receiverIndex]
        dealer = dealers[dealerIndex]

        def r(card): return process(card, receiver)
        def d(card): return process(card, dealer)
        w = leher(r, d)

        if w == Winner.Dealer:
          dealersPoints[dealerIndex] += 1
          receiversPoints[receiverIndex] -= 1
        else:
          receiversPoints[receiverIndex] += 1
          dealersPoints[receiverIndex] -= 1

        done += 1
      # percent = int(done / total * 100)
      # if percent % 25 == 0:
      #   print('progress: {0}%'.format(percent))

  print(sorted(receiversPoints)[-5:])
  print(sorted(dealersPoints)[-5:])

  receiversWithPoints = list(
      map(lambda t: (t[0], t[1], receiversPoints[t[0]]), enumerate(receivers)))
  dealersWithPoints = list(map(lambda t: (t[0], t[1], dealersPoints[t[0]]), enumerate(dealers)))

  receiversWithPoints.sort(key=operator.itemgetter(2))
  dealersWithPoints.sort(key=operator.itemgetter(2))

  bestReceivers = list(map(lambda t: t[1], receiversWithPoints))[-bestSize:]
  bestDealers = list(map(lambda t: t[1], dealersWithPoints))[-bestSize:]

  teachRound -= 1
  if teachRound <= 0:
    return (bestReceivers, bestDealers)

  return teach(bestReceivers, bestDealers, roundsCount, bestSize, newSize, childPerBest, teachRound, gameIndex + 1)


res = teach()

print("Final")
print(res[0][-1], res[1][-1])
