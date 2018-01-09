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


    def test_decode_posit_binary_normal(self):
        bits = 0x0025       # nbits=6, es=2, value=-128
        rep = decode_posit_binary(bits, 6, 2)
        self.assertEqual(rep, { 's': 1, 'k': 1, 'e': 3, 'f': 0, 'h': 0, 'nbits': 6, 'es': 2, 't': 'n' })

        bits = 0x0009       # nbits=6, es=2, value=3/32
        rep = decode_posit_binary(bits, 6, 2)
        self.assertEqual(rep, { 's': 0, 'k': -1, 'e': 0, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' })

        bits = 0x0015       # nbits=6, es=2, value=6
        rep = decode_posit_binary(bits, 6, 2)
        self.assertEqual(rep, { 's': 0, 'k': 0, 'e': 2, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' })


    def test_encode_posit_binary_special(self):
        # zero
        rep = { 's': 1, 'k': 1, 'e': 3, 'f': 0, 'h': 0, 'nbits': 6, 'es': 2, 't': 'z' }
        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 0)

        rep = { 's': 0, 'k': -1, 'e': 0, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' }
        bits = encode_posit_binary(rep)
        self.assertNotEqual(bits, 0)

        # cinf
        rep = { 's': 0, 'k': 0, 'e': 0, 'f': 0, 'h': 0, 'nbits': 10, 'es': 3, 't': 'c' }
        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 0x0200)

        rep = { 's': 1, 'k': 1, 'e': 0, 'f': 0, 'h': 0, 'nbits': 10, 'es': 3, 't': 'n' }
        bits = encode_posit_binary(rep)
        self.assertNotEqual(bits, 0x0200)


    def test_encode_posit_binary_normal(self):
        rep = { 's': 1, 'k': 1, 'e': 3, 'f': 0, 'h': 0, 'nbits': 6, 'es': 2, 't': 'n' }
        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 0x0025)

        rep = { 's': 0, 'k': -1, 'e': 0, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' }
        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 0x0009)

        rep = { 's': 0, 'k': 0, 'e': 2, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' }
        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 0x0015)


    def test_positrep_to_str(self):
        rep = { 's': 1, 'k': 1, 'e': 3, 'f': 0, 'h': 0, 'nbits': 6, 'es': 2, 't': 'n' }
        repstr = positrep_to_str(rep)
        self.assertEqual(repstr, '-128')

        rep = { 's': 0, 'k': -1, 'e': 0, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' }
        repstr = positrep_to_str(rep)
        self.assertEqual(repstr, '3/32')

        rep = { 's': 0, 'k': 0, 'e': 2, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' }
        repstr = positrep_to_str(rep)
        self.assertEqual(repstr, '6')

        rep = { 's': 0, 'k': 0, 'e': 0, 'f': 1, 'h': 1, 'nbits': 6, 'es': 2, 't': 'n' }
        repstr = positrep_to_str(rep)
        self.assertEqual(repstr, '1+1/2')

        rep = { 's': 0, 'k': 0, 'e': 0, 'f': 0, 'h': 0, 'nbits': 10, 'es': 3, 't': 'c' }
        repstr = positrep_to_str(rep)
        self.assertEqual(repstr, 'cinf')

        rep = { 's': 1, 'k': 1, 'e': 3, 'f': 0, 'h': 0, 'nbits': 6, 'es': 2, 't': 'z' }
        repstr = positrep_to_str(rep)
        self.assertEqual(repstr, '0')


    def test_encoding_decoding_symmetry_n6es2(self):
        nbits = 6
        es = 2
        for bits in range(2**nbits):
            rep = decode_posit_binary(bits, nbits, es)
            encoded_bits = encode_posit_binary(rep)
            self.assertEqual(encoded_bits, bits)


    def test_create_zero_positrep(self):
        nbits = 6
        es = 2
        rep = create_zero_positrep(nbits, es)
        self.assertEqual(rep['t'], 'z')

        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 0)


    def test_create_cinf_positrep(self):
        nbits = 6
        es = 2
        rep = create_cinf_positrep(nbits, es)
        self.assertEqual(rep['t'], 'c')

        bits = encode_posit_binary(rep)
        self.assertEqual(bits, 1 << (nbits-1))


if __name__ == '__main__':
    unittest.main()
