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

from sgposit.coder import *


class TestCoder(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_decode_posit_binary_special(self):
        # zero
        bits = 0
        rep = decode_posit_binary(bits, 8, 1)
        self.assertEqual(rep['t'], 'z')

        bits = 0x00AC
        rep = decode_posit_binary(bits, 16, 2)
        self.assertNotEqual(rep['t'], 'z')

        # cinf
        bits = 0x8000
        rep = decode_posit_binary(bits, 16, 3)
        self.assertEqual(rep['t'], 'c')

        bits = 0x400000
        rep = decode_posit_binary(bits, 23, 1)
        self.assertEqual(rep['t'], 'c')

        bits = 0x60000
        rep = decode_posit_binary(bits, 19, 1)
        self.assertNotEqual(rep['t'], 'c')

        bits = 0x0022
        rep = decode_posit_binary(bits, 6, 0)
        self.assertNotEqual(rep['t'], 'c')


if __name__ == '__main__':
    unittest.main()
