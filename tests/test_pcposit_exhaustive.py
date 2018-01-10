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


from __future__ import division

import os
import unittest

from mpmath import mp

from sgposit         import bitops
from sgposit         import coder
from sgposit.pcposit import PCPosit


class TestPCPositExhaustive(unittest.TestCase):

    _multiprocess_can_split_ = True


    def setUp(self):
        mp.dps = 1000


    def tearDown(self):
        pass


    def run_posit_1op_exhaustive(self, op_str=None, nbits_range=None, es_range=None):
        raise NotImplementedError


    # (a op b) rounded to nearest tests, with reference to mpmath computed results.
    def run_posit_2op_exhaustive(self, op_str=None, nbits_range=None, es_range=None):
        op = None
        mpop = None
        if op_str == '+':
            op = PCPosit.__add__
            mpop = mp.mpf.__add__
        elif op_str == '-':
            op = PCPosit.__sub__
            mpop = mp.mpf.__sub__
        elif op_str == '*':
            op = PCPosit.__mul__
            mpop = mp.mpf.__mul__
        elif op_str == '/':
            op = PCPosit.__truediv__
            mpop = mp.mpf.__truediv__
        else:
            raise NotImplementedError("op={}".format(op_str))

        for nbits in nbits_range:
          mask = bitops.create_mask(nbits)
          for es in es_range:
            for abits in range(2**nbits):
              for bbits in range(2**nbits):
                  a = PCPosit(abits, nbits=nbits, es=es, mode='bits')
                  b = PCPosit(bbits, nbits=nbits, es=es, mode='bits')
                  c = op(a, b)

                  if a.rep['t'] == 'n' and b.rep['t'] == 'n':
                      amp = mp.mpf(eval(coder.positrep_to_str(a.rep)))
                      bmp = mp.mpf(eval(coder.positrep_to_str(b.rep)))
                      c2mp = mpop(amp, bmp)
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


    @unittest.skipUnless(os.environ.get('SGPOSIT_LONG_TESTS') == '1', 'Long test.')
    def test_add_exhaustive(self):
        self.run_posit_2op_exhaustive('+', nbits_range=range(2,9), es_range=range(0,3))

    @unittest.skipUnless(os.environ.get('SGPOSIT_LONG_TESTS') == '1', 'Long test.')
    def test_sub_exhaustive(self):
        self.run_posit_2op_exhaustive('-', nbits_range=range(2,9), es_range=range(0,3))

    @unittest.skipUnless(os.environ.get('SGPOSIT_LONG_TESTS') == '1', 'Long test.')
    def test_mul_exhaustive(self):
        self.run_posit_2op_exhaustive('*', nbits_range=range(2,9), es_range=range(0,3))

    @unittest.skipUnless(os.environ.get('SGPOSIT_LONG_TESTS') == '1', 'Long test.')
    def test_truediv_exhaustive(self):
        self.run_posit_2op_exhaustive('/', nbits_range=range(2,9), es_range=range(0,3))


if __name__ == '__main__':
    unittest.main()
