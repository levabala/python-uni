class Rational:
  def __init__(self, nom, denom):
    self.nom = nom
    self.denom = denom

  def add(self, r):
    denom = r.denom * self.denom
    nom = r.nom * self.denom + self.nom * r.denom

    return Rational(nom, denom)


r1 = Rational(1, 3)
r2 = Rational(1, 2)

r3 = r1.add(r2)

print(r3.nom, '/', r3.denom)
