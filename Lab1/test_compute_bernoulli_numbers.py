import unittest
from main import compute_bernoulli_numbers

class TestComputeBernoulliNumbers(unittest.TestCase):
    def test_bernoulli_number_values(self):
        """Test specific Bernoulli number values against known values."""
        bernoulli_gen = compute_bernoulli_numbers()
        # Known Bernoulli numbers B_0 to B_10
        known_values = {
            0: 1,
            1: -0.5,
            2: 1 / 6,
            4: -1 / 30,
            6: 1 / 42,
            8: -1 / 30,
            10: 5 / 66
        }

        actual_values = {n: next(bernoulli_gen) for n in range(11)}

        for n, expected_value in known_values.items():
            with self.subTest(n=n):
                self.assertAlmostEqual(actual_values[n], expected_value, places=9)

if __name__ == '__main__':
    unittest.main()
