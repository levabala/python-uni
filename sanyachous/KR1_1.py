x = int(input("enter x "))
y = int(input("enter y "))
z = -1
if (y >= 0 and x**2+y**2 <= 1) or (x >= -2 and x <= 0 and y >= -1 and y <= 1):
  z = 1

print(z)
