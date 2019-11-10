import unittest
from unittest.mock import patch, Mock

from random_choice import search_interval, accumulate, random_choice

TOL = 1e-8


def almost_sequence_equal(actual, desired):
    if len(actual) != len(desired):
        raise AssertionError(f"{actual!r} should equal {desired!r}")
    if any(abs(x - y) > TOL for x, y in zip(actual, desired)):
        raise AssertionError(f"{actual!r} should equal {desired!r}")


class TestRandomChoice(unittest.TestCase):

    def test_search_interval(self):
        # has only one interval to search
        self.assertEqual(search_interval([1], 1), 0)
        self.assertEqual(search_interval([1], 0), 0)
        # x out of range
        self.assertRaises(ValueError, search_interval, [0.2, 0.5], 1)
        # best case
        self.assertEqual(search_interval([0.2, 0.5, 0.8, 0.9, 0.95, 1], 0.9), 3)
        # worst case
        self.assertEqual(search_interval([0.001 * x for x in range(1, 100)], 5e-4), 0)
        # negative intervals
        self.assertEqual(search_interval([-5, -2, 0], -7), 0)

    def test_accumulate(self):
        # single element
        self.assertEqual(list(accumulate([1])), [1])
        # multiple elements
        # -- float
        almost_sequence_equal(list(accumulate([0.2] * 3)), [0.2, 0.4, 0.6])
        almost_sequence_equal(list(accumulate([2.6, -1.9, 3.5])), [2.6, 0.7, 4.2])
        # -- integer
        almost_sequence_equal(list(accumulate([2, 5, 6])), [2, 7, 13])
        almost_sequence_equal(list(accumulate([-5, -3, 0])), [-5, -8, -8])
        # -- string
        self.assertEqual(list(accumulate(['abc', 'de', 'f'])), ['abc', 'abcde', 'abcdef'])

    # --------------- test random choice ---------------
    def test_random_choice_polutation_aint_sequence(self):
        self.assertRaises(TypeError, random_choice, 1, [0.5])

    def test_random_choice_items_weights_mismatch(self):
        self.assertRaises(ValueError, random_choice, ['item0', 'item1'], [0.5])

    def test_random_choice_invalid_k(self):
        self.assertRaises(ValueError, random_choice, [1, 2], [0.2, 0.3], -5)
        self.assertRaises(ValueError, random_choice, [1, 2], [0.2, 0.3], 0)
        self.assertRaises(TypeError, random_choice, [1, 2], [0.2, 0.3], 2.5)

    @patch('random_choice.random.random', Mock(side_effect=[0.1 * x for x in range(10)]))
    def test_random_choice_weights_sum_not_1(self):
        self.assertEqual(random_choice([4, 5, 6], [2.7, 6, 9], 3), [4, 4, 5])

    @patch('random_choice.random.random', Mock(side_effect=[0.1 * x for x in range(10)]))
    def test_random_choice_multiple_0s_in_weights(self):
        self.assertEqual(random_choice([0, 1, 2, 3], [0, 4, 0, 0], 5), [1, 1, 1, 1, 1])

    # only one item with weight 0.5
    @patch('random_choice.random.random', Mock(side_effect=[0.1 * x for x in range(10)]))
    def test_random_choice_single_item(self):
        self.assertEqual(random_choice(['item0'], [0.5], 5), ['item0'] * 5)

    # three items with weights ```[0.2, 0.3, 0.5]'''
    @patch('random_choice.random.random', Mock(side_effect=[0.1 * x for x in range(10)] * 2))
    def test_random_choice(self):
        self.assertEqual(random_choice([0, 1, 2], [0.2, 0.3, 0.5], 10), [0, 0, 0, 1, 1, 1, 2, 2, 2, 2])
        # no pre-defined weights
        self.assertEqual(random_choice([0, 1, 2], k=10), [0, 0, 0, 0, 1, 1, 1, 2, 2, 2])


if __name__ == '__main__':
    unittest.main()


