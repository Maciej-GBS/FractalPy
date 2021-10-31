from fractal.Julia import Julia as J
from fractal.Polynomial import Polynomial as P

j = J()
a = P([1, 0, 3, 4, 5])
b = P([1, 2, 2, 1, 3])
j.setDenominator(b)
j.setNumerator(a)
print(j)