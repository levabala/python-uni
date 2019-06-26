import matplotlib.pyplot as plt


def whenToTake(nonRefundableTicketCost, refundableTicketCost, refundCost):
  nonRefundLoss = nonRefundableTicketCost
  refundLoss = refundCost + (refundableTicketCost - nonRefundableTicketCost)

  threshold = 1 / (refundLoss / nonRefundLoss + 1)

  averageLoss = refundLoss * threshold

  print("nonRefundLoss: {0}".format(nonRefundLoss))
  print("refundLoss: {0}".format(refundLoss))
  print("threshold: {0}%".format(round(threshold * 100, 1)))
  print("average loss: {0:.2f}".format(averageLoss))

  horizontal = [n / 100 for n in range(101)]
  vertical1 = [refundLoss * (x) for x in horizontal]
  vertical2 = [nonRefundLoss * (1 - x) for x in horizontal]

  plt.scatter(horizontal, vertical1)
  plt.scatter(horizontal, vertical2)

  lines = plt.plot([threshold, threshold], [nonRefundLoss, 0])
  plt.setp(lines, color='green', linewidth=2.0)

  plt.show()


whenToTake(21000, 28000, 6000)
