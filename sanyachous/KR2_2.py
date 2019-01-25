e = int(input())
x = 1
y = (x+1)/(5*x+2)

while abs(y-x) >= e:
  x = y
  y = (x+1)/(5*x+2)

print(y)
