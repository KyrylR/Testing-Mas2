import unittest
from main import compute_ln_sin_x
import math
from unittest.mock import patch

class TestComputeLnSinX(unittest.TestCase):
    def test_valid_inputs(self):
        """Test compute_ln_sin_x with valid x and e values."""
        test_cases = [
            {'x': math.pi / 4, 'e': 0.01},
            {'x': math.pi / 6, 'e': 0.0001},
            {'x': -math.pi / 3, 'e': 0.001},
            {'x': math.pi / 2 - 0.01, 'e': 0.00001},
        ]
        for case in test_cases:
            with self.subTest(x=case['x'], e=case['e']):
                f_x_e, N = compute_ln_sin_x(case['x'], case['e'])
                # Compare with math.log(abs(math.sin(x)))
                expected_value = math.log(abs(math.sin(case['x'])))
                self.assertAlmostEqual(f_x_e, expected_value, places=2)

    def test_invalid_x_values(self):
        """Test compute_ln_sin_x with invalid x values."""
        invalid_x_values = [0, math.pi, -math.pi, 2 * math.pi]
        e = 0.001
        for x in invalid_x_values:
            with self.subTest(x=x):
                with self.assertRaises(ValueError):
                    compute_ln_sin_x(x, e)

    def test_invalid_e_values(self):
        """Test compute_ln_sin_x with invalid e values."""
        x = math.pi / 4
        invalid_e_values = [0, -0.01, 1, 2]
        for e in invalid_e_values:
            with self.subTest(e=e):
                with self.assertRaises(ValueError):
                    compute_ln_sin_x(x, e)

    def test_edge_cases(self):
        """Test compute_ln_sin_x with edge cases for x approaching 0 and π/2."""
        # x approaching 0
        x_values = [1e-8, 1e-6, 1e-4]
        e = 1e-5
        for x in x_values:
            with self.subTest(x=x):
                f_x_e, N = compute_ln_sin_x(x, e)
                expected_value = math.log(abs(math.sin(x)))
                self.assertAlmostEqual(f_x_e, expected_value, places=4)

        # x approaching π/2 from below
        x_values = [math.pi / 2 - 0.1, math.pi / 2 - 0.01, math.pi / 2 - 0.001]
        for x in x_values:
            with self.subTest(x=x):
                f_x_e, N = compute_ln_sin_x(x, e)
                expected_value = math.log(abs(math.sin(x)))

                print(f"X: {x}, Expected: {expected_value}, Actual: {f_x_e}")

                self.assertAlmostEqual(f_x_e, expected_value, places=4)

    def test_large_N(self):
        """Test compute_ln_sin_x with very small e to ensure large N is handled."""
        x = math.pi / 6
        e = 1e-15
        f_x_e, N = compute_ln_sin_x(x, e)
        self.assertTrue(N > 0)
        expected_value = math.log(abs(math.sin(x)))
        self.assertAlmostEqual(f_x_e, expected_value, places=12)

    def test_cannot_achieve_precision(self):
        """Test compute_ln_sin_x with very small e where precision cannot be achieved."""
        x = math.pi / 6
        e = 1e-100  # Very small e, likely to cause inability to achieve precision
        with self.assertRaises(ValueError):
            compute_ln_sin_x(x, e)

    def test_timeout(self):
        """Test compute_ln_sin_x to trigger a TimeoutError using time mocking."""
        x = math.pi / 6
        e = 1e-10  # Small e to ensure computation takes longer
        with patch('time.time', side_effect=[0, 15*60 + 1]):
            with self.assertRaises(TimeoutError):
                compute_ln_sin_x(x, e)

if __name__ == '__main__':
    unittest.main()
