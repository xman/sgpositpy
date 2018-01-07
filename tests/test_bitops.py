# MIT License
#
# Copyright (c) 2018 SpeedGo Computing
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import unittest

from sgposit.bitops import *


class TestBitops(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_create_mask(self):
        mask = create_mask(10)
        self.assertEqual(mask, 0x03FF)

        mask = create_mask(17)
        self.assertEqual(mask, 0x1FFFF)


    def test_get_int_bits(self):
        bits = get_int_bits(0x00FF, 3, 7)
        self.assertEqual(bits, 0x01F)

        bits = get_int_bits(0xFF0F, 4, 11)
        self.assertEqual(bits, 0x0F0)


    def test_count_leading_bits(self):
        bits = 0b0111110000
        self.assertEqual(count_leading_bits(bits, 1, 8), 5)

        bits = 0b0110001111
        self.assertEqual(count_leading_bits(bits, 0, 5), 2)

        bits = 0b0110001111
        self.assertEqual(count_leading_bits(bits, 1, 5), 0)


if __name__ == '__main__':
    unittest.main()
