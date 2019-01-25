x = int(input())
y = int(input())
z = int(input())
if x >= y+z or y >= x+z or z >= x+y:
  k = 1
elif x**2 == y**2+z**2 or y**2 == x**2+z**2 or z**2 == y**2+x**2:
  k = 2
elif x**2 > y**2+z**2 or y**2 > x**2+z**2 or z**2 > y**2+x**2:
  k = 3
else:
  k = 4

if k == 1:
  print('треугольник не существует')
elif k == 3:
  print('треугольник существует, и он - тупоугольный')
else:
  print('треугольник существует, но он не тупоугольный')
