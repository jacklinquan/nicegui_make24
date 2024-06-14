"""Make 24 Solver."""

from fractions import Fraction
from itertools import permutations


class Make24Value:
    """Make 24 Value.

    The `val` property is the Fraction result value.
    The `history` property is the calculation string.
    """

    def __init__(self, val, history=None) -> None:
        self._val = Fraction(val)
        self._history = history or str(val)

    @property
    def val(self):
        return self._val

    @property
    def history(self):
        return self._history

    def __repr__(self) -> str:
        return self.history

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Make24Value):
            raise ValueError(
                f"`other` must be an instance of {self.__class__.__name__}!"
            )
        return self.val == other.val and self.history == other.history

    def __hash__(self) -> int:
        return hash((self.val, self.history))

    def __add__(self, other: object) -> object:
        return Make24Value(self.val + other.val, f"({self.history}+{other.history})")

    def __sub__(self, other: object) -> object:
        return Make24Value(self.val - other.val, f"({self.history}-{other.history})")

    def __mul__(self, other: object) -> object:
        return Make24Value(self.val * other.val, f"({self.history}*{other.history})")

    def __truediv__(self, other: object) -> object:
        if other.val == 0:
            raise ZeroDivisionError("Divisor can NOT be 0!")
        return Make24Value(self.val / other.val, f"({self.history}/{other.history})")


# There are at most 24*5*4*4*4=7680 different expressions can be made with 4 numbers
# 24: permutations of 4 numbers
# 5: parenthesis positions: ((12)3)4, ((12)(34)), (1(23))4, 1((23)4), 1(2(34))
# 4*4*4: 4 operators at 3 operator positions
def recur_get_all_result(values: tuple[Make24Value]) -> tuple[Make24Value]:
    """Recursively calculate all the results from `values`."""

    if len(values) < 2:
        return tuple(values)
    else:
        all_result = []
        two_vals_perms = tuple(permutations(values, 2))
        for a, b in two_vals_perms:
            two_vals_result = []
            two_vals_result.append(a + b)
            two_vals_result.append(a - b)
            two_vals_result.append(a * b)
            if b.val != 0:
                two_vals_result.append(a / b)
            rest_values = list(values)
            rest_values.remove(a)
            rest_values.remove(b)
            for item in two_vals_result:
                less_values = tuple(rest_values) + (item,)
                all_result.extend(recur_get_all_result(less_values))
        return tuple(set(all_result))


# Example: solve24(1, 4, 5, 6) -> ((4/(1-(5/6))), (6/((5/4)-1)))
def solve24(*nums):
    """Get all the results that equal to 24."""

    values = tuple(Make24Value(item) for item in nums)
    all_result = recur_get_all_result(values)
    all_result_24 = tuple(item for item in all_result if item.val == 24)
    return all_result_24


def print_solve24(*nums):
    res = solve24(*nums)
    for item in res:
        print(item)
    print(f"\nWith number(s) {nums},")
    print(f"There is/are {len(res)} solution(s) in total.")


if __name__ == "__main__":
    print_solve24(1, 4, 5, 6)
