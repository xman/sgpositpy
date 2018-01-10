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


import os
import unittest

from mpmath import mp

from sgposit         import bitops
from sgposit         import coder
from sgposit.pcposit import PCPosit


class TestPCPosit(unittest.TestCase):

    _multiprocess_can_split_ = True


    def setUp(self):
        mp.dps = 1000


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


    # (a op b) rounded to nearest tests, with reference to mpmath computed results.
    @unittest.skipUnless(os.environ.get('SGPOSIT_LONG_TESTS') == '1', 'Long test.')
    def test_add_exhaustive(self):
        for nbits in range(2,9):
          for es in range(0,3):
            mask = bitops.create_mask(nbits)
            for abits in range(2**nbits):
                for bbits in range(2**nbits):
                    a = PCPosit(abits, nbits=nbits, es=es, mode='bits')
                    b = PCPosit(bbits, nbits=nbits, es=es, mode='bits')
                    c = a + b

                    if a.rep['t'] == 'n' and b.rep['t'] == 'n':
                        amp = mp.mpf(eval(coder.positrep_to_str(a.rep)))
                        bmp = mp.mpf(eval(coder.positrep_to_str(b.rep)))
                        c2mp = amp + bmp
                        c0 = PCPosit((bbits-1) & mask, nbits=nbits, es=es, mode='bits')
                        c1 = PCPosit((bbits+1) & mask, nbits=nbits, es=es, mode='bits')

                        cbits = coder.encode_posit_binary(c.rep)
                        roundedc = coder.decode_posit_binary(cbits, nbits=nbits, es=es)

                        rcmp = mp.mpf(eval(coder.positrep_to_str(roundedc)))
                        cratiodiffmp = mp.fabs(mp.log(rcmp/c2mp)) if c2mp != 0 else mp.fabs(rcmp - c2mp)
                        cabsdiffmp = mp.fabs(rcmp - c2mp)
                        if c0.rep['t'] == 'n':
                            c0mp = mp.mpf(eval(coder.positrep_to_str(c0.rep)))
                            c0ratiodiffmp = mp.fabs(mp.log(c0mp/c2mp)) if c2mp != 0 else mp.fabs(c0mp - c2mp)
                            c0absdiffmp = mp.fabs(c0mp - c2mp)
                            self.assertTrue(cratiodiffmp <= c0ratiodiffmp or cabsdiffmp <= c0absdiffmp)
                        if c1.rep['t'] == 'n':
                            c1mp = mp.mpf(eval(coder.positrep_to_str(c1.rep)))
                            c1ratiodiffmp = mp.fabs(mp.log(c1mp/c2mp)) if c2mp != 0 else mp.fabs(c1mp - c2mp)
                            c1absdiffmp = mp.fabs(c1mp - c2mp)
                            self.assertTrue(cratiodiffmp <= c1ratiodiffmp or cabsdiffmp <= c1absdiffmp)


    def test_sub_simple(self):
        nbits = 6
        es = 2

        a = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        b = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        c = a - b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x00) #  0

        a = PCPosit(0x0C, nbits=nbits, es=es, mode='bits')  #  1/4
        b = PCPosit(0x0F, nbits=nbits, es=es, mode='bits')  #  3/4
        c = a - b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x32) # -1/2

        a = PCPosit(0x0A, nbits=nbits, es=es, mode='bits')  #  1/8
        b = PCPosit(0x35, nbits=nbits, es=es, mode='bits')  # -3/16
        c = a - b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x0C) #  5/16 ~> 1/4

        a = PCPosit(0x0D, nbits=nbits, es=es, mode='bits')  #  3/8
        b = PCPosit(0x0F, nbits=nbits, es=es, mode='bits')  #  3/4
        c = a - b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x33) # -3/8

        a = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        b = PCPosit(0x10, nbits=nbits, es=es, mode='bits')  #  1
        c = a - b
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x0E) #  1/2


    # (a op b) rounded to nearest tests, with reference to mpmath computed results.
    @unittest.skipUnless(os.environ.get('SGPOSIT_LONG_TESTS') == '1', 'Long test.')
    def test_mul_exhaustive(self):
        for nbits in range(2,9):
          for es in range(0,3):
            mask = bitops.create_mask(nbits)
            for abits in range(2**nbits):
                for bbits in range(2**nbits):
                    a = PCPosit(abits, nbits=nbits, es=es, mode='bits')
                    b = PCPosit(bbits, nbits=nbits, es=es, mode='bits')
                    c = a * b

                    if a.rep['t'] == 'n' and b.rep['t'] == 'n':
                        amp = mp.mpf(eval(str(a)))
                        bmp = mp.mpf(eval(str(b)))
                        c2mp = amp * bmp
                        c0 = PCPosit((bbits-1) & mask, nbits=nbits, es=es, mode='bits')
                        c1 = PCPosit((bbits+1) & mask, nbits=nbits, es=es, mode='bits')

                        rcmp = mp.mpf(eval(str(c)))
                        cratiodiffmp = mp.fabs(mp.log(rcmp/c2mp)) if c2mp != 0 else mp.fabs(rcmp - c2mp)
                        cabsdiffmp = mp.fabs(rcmp - c2mp)
                        if c0.rep['t'] == 'n':
                            c0mp = mp.mpf(eval(str(c0)))
                            c0ratiodiffmp = mp.fabs(mp.log(c0mp/c2mp)) if c2mp != 0 else mp.fabs(c0mp - c2mp)
                            c0absdiffmp = mp.fabs(c0mp - c2mp)
                            self.assertTrue(cratiodiffmp <= c0ratiodiffmp or cabsdiffmp <= c0absdiffmp)
                        if c1.rep['t'] == 'n':
                            c1mp = mp.mpf(eval(str(c1)))
                            c1ratiodiffmp = mp.fabs(mp.log(c1mp/c2mp)) if c2mp != 0 else mp.fabs(c1mp - c2mp)
                            c1absdiffmp = mp.fabs(c1mp - c2mp)
                            self.assertTrue(cratiodiffmp <= c1ratiodiffmp or cabsdiffmp <= c1absdiffmp)


    def test_neg_simple(self):
        nbits = 6
        es = 2

        a = PCPosit(0x11, nbits=nbits, es=es, mode='bits')  #  3/2
        c = -a
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x2F) # -3/2

        a = PCPosit(0x35, nbits=nbits, es=es, mode='bits')  # -3/16
        c = -a
        cbits = coder.encode_posit_binary(c.rep)
        self.assertEqual(cbits, 0x0B) # 3/16


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
