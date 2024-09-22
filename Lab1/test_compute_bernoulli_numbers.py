import unittest
from main import compute_bernoulli_numbers

class TestComputeBernoulliNumbers(unittest.TestCase):
    def test_valid_n_max(self):
        """Test compute_bernoulli_numbers with valid n_max values."""
        n_max_values = [0, 1, 2, 5, 10, 20]
        for n_max in n_max_values:
            with self.subTest(n_max=n_max):
                B = compute_bernoulli_numbers(n_max)
                self.assertEqual(len(B), n_max + 1)

    def test_bernoulli_number_values(self):
        """Test specific Bernoulli number values against known values."""
        n_max = 10
        B = compute_bernoulli_numbers(n_max)
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
        for n, expected_value in known_values.items():
            with self.subTest(n=n):
                self.assertAlmostEqual(B[n], expected_value, places=9)

    def test_invalid_n_max(self):
        """Test compute_bernoulli_numbers with invalid n_max values."""
        invalid_n_max_values = [-1, -10, 'a', None]
        for n_max in invalid_n_max_values:
            with self.subTest(n_max=n_max):
                with self.assertRaises(ValueError):
                    compute_bernoulli_numbers(n_max)

    def test_large_n_max(self):
        """Test compute_bernoulli_numbers with a large n_max value."""
        n_max = 1000
        B = compute_bernoulli_numbers(n_max)
        self.assertEqual(len(B), n_max + 1)

if __name__ == '__main__':
    unittest.main()
