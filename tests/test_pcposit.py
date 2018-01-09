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
        pass


    def tearDown(self):
        pass


    # Simple cases for bits to bits comparisons.
    def test_add_simple(self):
        nbits = 6
        es = 2

        a = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        b = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        c = a + b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x13) # 3

        a = PCPosit(0x0C, nbits=nbits, es=es, mode='bits')  #  1/4
        b = PCPosit(0x0F, nbits=nbits, es=es, mode='bits')  #  3/4
        c = a + b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x10) # 1

        a = PCPosit(0x0A, nbits=nbits, es=es, mode='bits')  #  1/8
        b = PCPosit(0x35, nbits=nbits, es=es, mode='bits')  # -3/16
        c = a + b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x38) # -1/16

        a = PCPosit(0x0D, nbits=nbits, es=es, mode='bits')  #  3/8
        b = PCPosit(0x0F, nbits=nbits, es=es, mode='bits')  #  3/4
        c = a + b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x10) # 9/8 ~> 1

        a = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        b = PCPosit(0x10, nbits=nbits, es=es, mode='bits')  #  1
        c = a + b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x12) # 2+1/2 ~> 2


    @unittest.skip("Not implemented.")
    def test_sub(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_neg(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_mul(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_truediv(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_floordiv(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_eq(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_ne(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_lt(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_le(self):
        raise NotImplementedError


    @unittest.skip("Not implemented.")
    def test_gt(self):
        raise NotImplementedError


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
