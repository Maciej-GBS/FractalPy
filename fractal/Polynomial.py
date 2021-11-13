import numpy as np
import re

from typing import Union


class Polynomial:
    def __init__(self, factors: Union[str, list] = [0]):
        if isinstance(factors, str):
            self.from_str(factors)
        else:
            self._poly = np.poly1d(factors, variable='x')

    def from_str(self, factorstr: str):
        poly = []
        def add_atom(atom, p):
            while len(poly) <= p:
                poly.append(complex(0.0))
            poly[len(poly) - 1 - p] += atom
        truncated = factorstr.replace(" ", "")
        patterns = [
            "[\-]?[(][0-9.j+\-]*[)]x[0-9^]{2,}",
            "[\-]?[(][0-9.j+\-]*[)]x",
            "[\-]?[(][0-9.j+\-]*[)]",
            "[0-9.j\-]*x[0-9^]{2,}",
            "[0-9.j\-]*x",
            "[0-9.j\-]+"
        ]
        fix_sign = lambda s: s.replace("-(","(-").replace("--","-")
        for regex in patterns:
            matches = re.findall(regex, truncated)
            for x in matches:
                truncated = truncated.replace(x, "")
                if 'x^' in x:
                    sides = x.split('x^')
                    add_atom(complex(fix_sign(sides[0])), int(sides[1]))
                elif 'x' in x:
                    sides = x.split('x')
                    add_atom(complex(fix_sign(sides[0])), 1)
                else:
                    add_atom(complex(x), 0)
        self._poly = np.poly1d(poly, variable='x')

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self._poly == other._poly
        return self._poly == other

    def __call__(self, x: complex):
        return self.calc(x)

    def __len__(self):
        return self._poly.order + 1

    def __getitem__(self, key: int):
        return self._poly.coeffs[key]

    def __setitem__(self, key: int, value):
        self._poly.coeffs[key] = value

    def __iter__(self):
        return iter(self._poly.coeffs)

    def __str__(self):
        atom_list = []
        for index, c in enumerate(self._poly.coeffs):
            if c == 0:
                continue

            # Non-zero coefficients
            atom = f"{c}"

            # Meaningful powers
            if index < self._poly.order:
                atom += f"{self._poly.variable}"
            if index + 1 < self._poly.order:
                atom += f"^{self._poly.order - index}"
            atom_list.append(atom)
        return " + ".join(atom_list)

    def calc(self, x: complex):
        """Calculate polynomial's 'y' value at point 'x': P(x) = y

        Args:
            x (complex): argument to polynomial function
        """
        return self._poly(x)
