n = int(input())
a = [0] + [0] * (n-1)
b = [1] + [0] * (n-1)

for i in range(1, n):
  a[i] = b[i-1]-a[i-1]
  b[i] = a[i-1]+b[i-1]

k = 1

for i in range(k+1, n):
  c = (-1)**k / (2*a[i]+b[i])

print(c)
