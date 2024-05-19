import unittest
import discrete
import string


class TestDiscrete(unittest.TestCase):
    def test_cross(self):
        A = [1, 2, 3]
        B = ['x', 'y']
        C = discrete.cross(A, B)

        self.assertTrue(isinstance(C, set))
        self.assertTrue(len(C) == len(A) * len(B))
        self.assertTrue('1x' in C)

    def test_all_combos(self):
        S = [str(c) for c in string.ascii_lowercase[0:5]]
        X = discrete.all_combos(S, 2)

        self.assertTrue(isinstance(X, set))
        self.assertTrue(len(X) == 10)
        self.assertTrue('a b' in X or 'b a' in X)

    def test_such_that(self):
        def is_even(n): return n % 2 == 0
        X = {n for n in range(11)}
        Y = discrete.such_that(is_even, X)

        self.assertTrue(len(Y) == 6)
        for n in range(0, 11, 2):
            self.assertTrue(n in Y)


if __name__ == '__main__':
    unittest.main()
