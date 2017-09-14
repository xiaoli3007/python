from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.


import unittest


def division_funtion(x, y):
    return x / y


class TestDivision(unittest.TestCase):
    def test_int(self):
        self.assertEqual(division_funtion(19, 3), 3)

    def test_int2(self):
        self.assertEqual(division_funtion(119, 4), 2.25)

    def test_float(self):
        self.assertEqual(division_funtion(114.2, 3), 1.4)


if __name__ == '__main__':
    unittest.main()
