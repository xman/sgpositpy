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

from sgposit         import coder
from sgposit.pcposit import PCPosit


class TestPCPosit(unittest.TestCase):

    def setUp(self):
        self.posit_n6e2_m1o16_bits = 0x38
        self.posit_n6e2_m1o2_bits = 0x32
        self.posit_n6e2_m1o64_bits = 0x3A
        self.posit_n6e2_m3o2_bits = 0x2F
        self.posit_n6e2_m3o4_bits = 0x31
        self.posit_n6e2_m3o8_bits = 0x33
        self.posit_n6e2_m3o16_bits = 0x35

        self.posit_n6e2_1_bits = 0x10
        self.posit_n6e2_1o2_bits = 0x0E
        self.posit_n6e2_1o4_bits = 0x0C
        self.posit_n6e2_1o8_bits = 0x0A
        self.posit_n6e2_2_bits = 0x12
        self.posit_n6e2_3_bits = 0x13
        self.posit_n6e2_3o2_bits = 0x11
        self.posit_n6e2_3o4_bits = 0x0F
        self.posit_n6e2_3o16_bits = 0x0B
        self.posit_n6e2_3o8_bits = 0x0D
        self.posit_n6e2_cinf_bits = 0x20


    def tearDown(self):
        pass


    def run_posit_op(self, abits=None, op_str=None, bbits=None, ref_cbits=None, nbits=None, es=None):
        a = PCPosit(abits, nbits=nbits, es=es, mode='bits')
        b = PCPosit(bbits, nbits=nbits, es=es, mode='bits')
        c = None

        if op_str == '+':
            c = a + b
        elif op_str == '-':
            c = a - b
        elif op_str == '*':
            c = a * b
        elif op_str == '/':
            c = a / b
        elif op_str == 'u-':
            c = -a
        else:
            raise NotImplementedError("op={}".format(op_str))

        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, ref_cbits)


    def test_add_simple(self):
        self.run_posit_op(self.posit_n6e2_3o2_bits, '+', self.posit_n6e2_3o2_bits, self.posit_n6e2_3_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o4_bits, '+', self.posit_n6e2_3o4_bits, self.posit_n6e2_1_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o8_bits, '+', self.posit_n6e2_m3o16_bits, self.posit_n6e2_m1o16_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o8_bits, '+', self.posit_n6e2_3o4_bits, self.posit_n6e2_1_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o2_bits, '+', self.posit_n6e2_1_bits, self.posit_n6e2_2_bits, 6, 2)


    def test_sub_simple(self):
        self.run_posit_op(self.posit_n6e2_3o2_bits, '-', self.posit_n6e2_3o2_bits, 0, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o4_bits, '-', self.posit_n6e2_3o4_bits, self.posit_n6e2_m1o2_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o8_bits, '-', self.posit_n6e2_m3o16_bits, self.posit_n6e2_1o4_bits, 6, 2) # result: 5/16 ~> 1/4
        self.run_posit_op(self.posit_n6e2_3o8_bits, '-', self.posit_n6e2_3o4_bits, self.posit_n6e2_m3o8_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o2_bits, '-', self.posit_n6e2_1_bits, self.posit_n6e2_1o2_bits, 6, 2)


    def test_neg_simple(self):
        self.run_posit_op(self.posit_n6e2_3o2_bits, 'u-', None, self.posit_n6e2_m3o2_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_m3o16_bits, 'u-', None, self.posit_n6e2_3o16_bits, 6, 2)


    def test_mul_simple(self):
        self.run_posit_op(self.posit_n6e2_3o2_bits, '*', self.posit_n6e2_3o2_bits, self.posit_n6e2_2_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o4_bits, '*', self.posit_n6e2_3o4_bits, self.posit_n6e2_3o16_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o8_bits, '*', self.posit_n6e2_m3o16_bits, self.posit_n6e2_m1o64_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o8_bits, '*', self.posit_n6e2_3o4_bits, self.posit_n6e2_1o4_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o2_bits, '*', self.posit_n6e2_1_bits, self.posit_n6e2_3o2_bits, 6, 2)


    def test_truediv_simple(self):
        self.run_posit_op(self.posit_n6e2_3o2_bits, '/', self.posit_n6e2_3o2_bits, self.posit_n6e2_1_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o4_bits, '/', self.posit_n6e2_3o4_bits, self.posit_n6e2_3o8_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_1o8_bits, '/', self.posit_n6e2_m3o16_bits, self.posit_n6e2_m3o4_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o8_bits, '/', self.posit_n6e2_3o4_bits, self.posit_n6e2_1o2_bits, 6, 2)
        self.run_posit_op(self.posit_n6e2_3o2_bits, '/', self.posit_n6e2_1_bits, self.posit_n6e2_3o2_bits, 6, 2)


    def test_create_pcposit_from_large_int_bits(self):
        p0 = PCPosit(3**80, mode='bits', nbits=256, es=2)
        p1 = PCPosit(5**90, mode='bits', nbits=256, es=2)
        p2 = p0 + p1
        p3 = p0 - p1
        p4 = p0 * p1
        p5 = p0 / p1


    @unittest.skip("Not implemented.")
    def test_floordiv(self):
        raise NotImplementedError


    def run_posit_cmp_op(self, abits=None, op_str=None, bbits=None, ref_output=None, nbits=None, es=None):
        a = PCPosit(abits, nbits=nbits, es=es, mode='bits')
        b = PCPosit(bbits, nbits=nbits, es=es, mode='bits')
        out = None

        if op_str == '==':
            out = (a == b)
        elif op_str == '!=':
            out = (a != b)
        elif op_str == '<':
            out = (a < b)
        elif op_str == '<=':
            out = (a <= b)
        elif op_str == '>':
            out = (a > b)
        elif op_str == '>=':
            out = (a >= b)
        else:
            raise NotImplementedError("op={}".format(op_str))

        self.assertEqual(out, ref_output)


    def test_eq(self):
        self.run_posit_cmp_op(0, '==', 0, True, 6, 2)
        self.run_posit_cmp_op(0, '==', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(0, '==', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(0, '==', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '==', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '==', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '==', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '==', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '==', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '==', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '==', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '==', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '==', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '==', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '==', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '==', self.posit_n6e2_m3o16_bits, True, 6, 2)


    def test_ne(self):
        self.run_posit_cmp_op(0, '!=', 0, False, 6, 2)
        self.run_posit_cmp_op(0, '!=', self.posit_n6e2_cinf_bits, True, 6, 2)
        self.run_posit_cmp_op(0, '!=', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(0, '!=', self.posit_n6e2_m3o16_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '!=', 0, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '!=', self.posit_n6e2_cinf_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '!=', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '!=', self.posit_n6e2_m3o16_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '!=', 0, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '!=', self.posit_n6e2_cinf_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '!=', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '!=', self.posit_n6e2_m3o16_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '!=', 0, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '!=', self.posit_n6e2_cinf_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '!=', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '!=', self.posit_n6e2_m3o16_bits, False, 6, 2)


    def test_lt(self):
        self.run_posit_cmp_op(0, '<', 0, False, 6, 2)
        self.run_posit_cmp_op(0, '<', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(0, '<', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(0, '<', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', 0, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_m1o16_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_3_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_1o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<', self.posit_n6e2_m3o4_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_m1o16_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_3_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_1o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<', self.posit_n6e2_m3o4_bits, False, 6, 2)


    def test_le(self):
        self.run_posit_cmp_op(0, '<=', 0, True, 6, 2)
        self.run_posit_cmp_op(0, '<=', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(0, '<=', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(0, '<=', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<=', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<=', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<=', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '<=', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', 0, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_3o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_m3o16_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_m1o16_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_3_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_1o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '<=', self.posit_n6e2_m3o4_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_m1o16_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_3_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_1o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '<=', self.posit_n6e2_m3o4_bits, False, 6, 2)


    def test_gt(self):
        self.run_posit_cmp_op(0, '>', 0, False, 6, 2)
        self.run_posit_cmp_op(0, '>', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(0, '>', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(0, '>', self.posit_n6e2_m3o16_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '>', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '>', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '>', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_cinf_bits, '>', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', 0, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_m3o16_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', 0, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_cinf_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_3o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_m3o16_bits, False, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_m1o16_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_3_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_1o2_bits, True, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_3o2_bits, '>', self.posit_n6e2_m3o4_bits, True, 6, 2)

        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_m1o16_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_3_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_1o2_bits, False, 6, 2)
        self.run_posit_cmp_op(self.posit_n6e2_m3o16_bits, '>', self.posit_n6e2_m3o4_bits, True, 6, 2)


    @unittest.skip("Not implemented.")
    def test_ge(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_str(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_repr(self):
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
