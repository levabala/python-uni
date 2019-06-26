import random
from enum import Enum


Winner = Enum("Winner", "Receiver Dealer")


def flat(l): return [item for sublist in l for item in sublist]


def leher(receiver, dealer):
  cards = list(flat(map(lambda n: [n] * 4, range(1, 14))))
  random.shuffle(cards)

  # random cards
  r = cards.pop()
  d = cards.pop()

  # ask reveiver if he wants to exchange cards (and checks if dealer's card is not a king)
  exchange = receiver(r) and d != 13

  # do or not to do the exchange
  if exchange:
    r, d = d, r

  # ask dealer to change his card (if next card is not a king)
  newCard = cards.pop()
  d = newCard if dealer(d) and newCard != 3 else d

  # check who won
  return Winner.Receiver if r > d else Winner.Dealer


leher(lambda a: False, lambda a: False)
