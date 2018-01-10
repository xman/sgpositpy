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


class TestCodingSymmetry(unittest.TestCase):

    def run_encoding_decoding_symmetry(self, nbits=None, es=None):
        for bits in range(2**nbits):
            rep = decode_posit_binary(bits, nbits, es)
            encoded_bits = encode_posit_binary(rep)
            self.assertEqual(encoded_bits, bits)


    def test_encoding_decoding_symmetry_n2e0(self):
        self.run_encoding_decoding_symmetry(nbits=2, es=0)
    def test_encoding_decoding_symmetry_n2e1(self):
        self.run_encoding_decoding_symmetry(nbits=2, es=1)
    def test_encoding_decoding_symmetry_n2e2(self):
        self.run_encoding_decoding_symmetry(nbits=2, es=2)
    def test_encoding_decoding_symmetry_n2e3(self):
        self.run_encoding_decoding_symmetry(nbits=2, es=3)

    def test_encoding_decoding_symmetry_n3e0(self):
        self.run_encoding_decoding_symmetry(nbits=3, es=0)
    def test_encoding_decoding_symmetry_n3e1(self):
        self.run_encoding_decoding_symmetry(nbits=3, es=1)
    def test_encoding_decoding_symmetry_n3e2(self):
        self.run_encoding_decoding_symmetry(nbits=3, es=2)
    def test_encoding_decoding_symmetry_n3e3(self):
        self.run_encoding_decoding_symmetry(nbits=3, es=3)
    def test_encoding_decoding_symmetry_n3e4(self):
        self.run_encoding_decoding_symmetry(nbits=3, es=4)

    def test_encoding_decoding_symmetry_n4e0(self):
        self.run_encoding_decoding_symmetry(nbits=4, es=0)
    def test_encoding_decoding_symmetry_n4e1(self):
        self.run_encoding_decoding_symmetry(nbits=4, es=1)
    def test_encoding_decoding_symmetry_n4e2(self):
        self.run_encoding_decoding_symmetry(nbits=4, es=2)
    def test_encoding_decoding_symmetry_n4e3(self):
        self.run_encoding_decoding_symmetry(nbits=4, es=3)
    def test_encoding_decoding_symmetry_n4e4(self):
        self.run_encoding_decoding_symmetry(nbits=4, es=4)
    def test_encoding_decoding_symmetry_n4e5(self):
        self.run_encoding_decoding_symmetry(nbits=4, es=5)

    def test_encoding_decoding_symmetry_n5e0(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=0)
    def test_encoding_decoding_symmetry_n5e1(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=1)
    def test_encoding_decoding_symmetry_n5e2(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=2)
    def test_encoding_decoding_symmetry_n5e3(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=3)
    def test_encoding_decoding_symmetry_n5e4(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=4)
    def test_encoding_decoding_symmetry_n5e5(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=5)
    def test_encoding_decoding_symmetry_n5e6(self):
        self.run_encoding_decoding_symmetry(nbits=5, es=6)

    def test_encoding_decoding_symmetry_n6e0(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=0)
    def test_encoding_decoding_symmetry_n6e1(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=1)
    def test_encoding_decoding_symmetry_n6e2(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=2)
    def test_encoding_decoding_symmetry_n6e3(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=3)
    def test_encoding_decoding_symmetry_n6e4(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=4)
    def test_encoding_decoding_symmetry_n6e5(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=5)
    def test_encoding_decoding_symmetry_n6e6(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=6)
    def test_encoding_decoding_symmetry_n6e7(self):
        self.run_encoding_decoding_symmetry(nbits=6, es=7)


if __name__ == '__main__':
    unittest.main()
