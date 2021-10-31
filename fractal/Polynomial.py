import numpy as np

from typing import Union


class Polynomial:
    def __init__(self, factors: Union[str, list] = [0]):
        if isinstance(factors, str):
            # TODO: parsing from string
            pass
        else:
            self._poly = np.poly1d(factors, variable='x')

    # def __init__(self, *factors: complex):
    #     pass

    def __call__(self, x: complex):
        return self.calc(x)

    def __len__(self):
        return self._poly.order + 1

    def __getitem__(self, key: int):
        return self._poly.coeffs[key]

    def __setitem__(self, key: int, value):
        self._poly.coeffs[key] = value

    def __iter__(self):
        return self._poly.coeffs.__iter__()

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
