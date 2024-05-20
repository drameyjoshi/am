import unittest
import discrete
import string
import math
import time

from fractions import Fraction


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
        self.assertTrue(len(X) == math.comb(5, 2))
        self.assertTrue('a b' in X or 'b a' in X)

    def test_such_that(self):
        def is_even(n): return n % 2 == 0
        X = {n for n in range(11)}
        Y = discrete.such_that(is_even, X)

        self.assertTrue(len(Y) == 6)
        for n in range(0, 11, 2):
            self.assertTrue(n in Y)

    def test_P_die(self):
        # Simple dice problems.
        D = {n for n in range(1, 7)}
        even = {n for n in range(2, 7, 2)}

        p_even = discrete.P(even, D)
        self.assertTrue(p_even == Fraction(1, 2))

        def is_even(n): return n % 2 == 0
        self.assertTrue(discrete.P(is_even, D) == Fraction(1, 2))

    @unittest.skipIf(1 == 1, 'Takes time, tested once.')
    def test_card(self):
        # Card problems
        suits = 'SHDC'
        ranks = 'A23456789TJQK'

        deck = discrete.cross(ranks, suits)
        self.assertTrue(len(deck) == 52)

        hands = discrete.all_combos(deck, 5)
        self.assertTrue(len(hands) == math.comb(52, 5))

        def flush(hand): return any(hand.count(s) == 5 for s in suits)
        t0 = time.time()
        self.assertTrue(discrete.P(flush, hands) == Fraction(33, 16660))
        t1 = time.time()

        def four_kind(hand): return any(hand.count(r) == 4 for r in ranks)
        t2 = time.time()
        self.assertTrue(discrete.P(four_kind, hands) == Fraction(1, 4165))
        t3 = time.time()

        print('Find probability of flush took ', t1 - t0, 'seconds')
        print('Find probability of 4 of a kind took ', t3 - t2, 'seconds')

    def test_pmf(self):
        # Babies in Denmark problem.
        data = {'GG': 121801, 'GB': 126840, 'BG': 127123, 'BB': 135138}
        denmark = discrete.Pmf(data)

        def first_girl(outcome): return outcome[0] == 'G'
        def first_boy(outcome): return outcome[0] == 'B'
        def second_girl(outcome): return outcome[1] == 'G'
        def second_boy(outcome): return outcome[1] == 'B'
        def two_girls(outcome): return outcome == 'GG'
        def two_boys(outcome): return outcome == 'BB'

        self.assertTrue(discrete.P(first_girl, denmark) >= 0.4866700)
        self.assertTrue(discrete.P(first_girl, denmark) <= 0.4866710)

        self.assertTrue(discrete.P(second_girl, denmark) >= 0.4872244)
        self.assertTrue(discrete.P(second_girl, denmark) <= 0.4872246)

        p_gg = discrete.P(second_girl, discrete.such_that(first_girl, denmark))
        self.assertTrue(p_gg >= 0.4898669)
        self.assertTrue(p_gg <= 0.4898670)

        p_gb = discrete.P(second_girl, discrete.such_that(first_boy, denmark))
        self.assertTrue(p_gb >= 0.4847194)
        self.assertTrue(p_gb <= 0.4847195)

        p_bg = discrete.P(second_boy, discrete.such_that(first_girl, denmark))
        self.assertTrue(p_bg >= 0.5101330)
        self.assertTrue(p_bg <= 0.5101331)

        p_bb = discrete.P(second_boy, discrete.such_that(first_boy, denmark))
        self.assertTrue(p_bb >= 0.5152805)
        self.assertTrue(p_bb <= 0.5152806)

    def test_join_pmf(self):
        # M&M problem from https://nbviewer.org/url/norvig.com/ipython/Probability.ipynb
        b94 = discrete.Pmf({'brown': 30, 'yellow': 20, 'red': 20,
                            'green': 10, 'orange': 10, 'tan': 10})
        b96 = discrete.Pmf({'blue': 24, 'green': 20, 'orange': 16,
                            'yellow': 14, 'red': 13, 'brown': 13})

        mnm = discrete.joint_pmf(b94, b96, ' ')

        def yellow_and_green(outcome):
            return 'yellow' in outcome and 'green' in outcome

        def yellow_94(outcome): return outcome.startswith('yellow')

        p_y94 = discrete.P(
            yellow_94, discrete.such_that(yellow_and_green, mnm))
        self.assertTrue(1 == 1)
        self.assertTrue(p_y94 > 0.74)


if __name__ == '__main__':
    unittest.main()
