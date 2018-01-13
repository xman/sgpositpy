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


import numbers

from sgposit import coder


"""
Provably correct posit number arithmetic.
"""
class PCPosit:

    def __init__(self, v=None, mode=None, nbits=None, es=None):
        nbits_given = True
        es_given = True
        if nbits is None:
            nbits_given = False
            nbits = 32
        if es is None:
            es_given = False
            es = 2

        if v is None:
            self.rep = coder.create_zero_positrep(nbits=nbits, es=es)
            return
        elif isinstance(v, PCPosit):
            if nbits_given and v.rep['nbits'] != nbits:
                raise NotImplementedError('Mismatched nbits posit conversion is not implemented.')
            if es_given and v.rep['es'] != es:
                raise NotImplementedError('Mismatched es posit conversion is not implemented.')
            self.rep = coder.copy_positrep(v.rep)
            return
        elif mode == 'bits':
            if isinstance(v, numbers.Integral):
                self.rep = coder.decode_posit_binary(v, nbits=nbits, es=es)
                return
            elif isinstance(v, str):
                raise NotImplementedError('Binary bit string posit conversion is not implemented.')
        elif isinstance(v, str):
            if v == 'cinf':
                self.rep = coder.create_cinf_positrep(nbits=nbits, es=es)
            elif v == '0':
                self.rep = coder.create_zero_positrep(nbits=nbits, es=es)
            else:
                raise ValueError('Expect 0 or cinf posit consntant from the input string.')

            return

        raise ValueError('Input is not supported.')


    def __add__(self, other):
        if self.rep['t'] == 'z':
            return PCPosit(other)
        elif other.rep['t'] == 'z':
            return PCPosit(self)
        elif self.rep['t'] == 'c' or other.rep['t'] == 'c':
            return PCPosit('cinf', nbits=self.rep['nbits'], es=self.rep['es'])

        assert self.rep['t'] == 'n' and other.rep['t'] == 'n'

        (xa,ma) = self._fixedpoint()
        (xb,mb) = other._fixedpoint()

        m = max(ma, mb)
        xc = xa*2**(m-mb) + xb*2**(m-ma)
        mc = ma + mb - m

        return self._fixedpoint_to_posit(xc, mc, nbits=self.rep['nbits'], es=self.rep['es'])


    def __sub__(self, other):
        p = -PCPosit(other)
        return self + p


    def __neg__(self):
        p = PCPosit(self)
        if p.rep['t'] == 'n':
            p.rep['s'] = p.rep['s'] ^ 1
        return p


    def __mul__(self, other):
        if self.rep['t'] == 'c' or other.rep['t'] == 'c':
            return PCPosit('cinf', nbits=self.rep['nbits'], es=self.rep['es'])
        elif self.rep['t'] == 'z' or other.rep['t'] == 'z':
            return PCPosit('0', nbits=self.rep['nbits'], es=self.rep['es'])

        assert self.rep['t'] == 'n' and other.rep['t'] == 'n'

        (xa,ma) = self._fixedpoint()
        (xb,mb) = other._fixedpoint()

        xc = xa * xb
        mc = ma + mb

        return self._fixedpoint_to_posit(xc, mc, nbits=self.rep['nbits'], es=self.rep['es'])


    def __div__(self, other):
        return self.__truediv__(other)


    def __truediv__(self, other):
        if self.rep['t'] == 'c' or other.rep['t'] == 'z':
            return PCPosit('cinf', nbits=self.rep['nbits'], es=self.rep['es'])
        elif self.rep['t'] == 'z' or other.rep['t'] == 'c':
            return PCPosit('0', nbits=self.rep['nbits'], es=self.rep['es'])

        assert self.rep['t'] == 'n' and other.rep['t'] == 'n'

        (xa,ma) = self._fixedpoint()
        (xb,mb) = other._fixedpoint()

        nbits = self.rep['nbits']
        es = self.rep['es']
        sign = 1
        if (xa < 0)^(xb < 0): sign = -1
        if xa < 0: xa = -xa
        if xb < 0: xb = -xb

        g = ma - mb + (2**es)*(nbits-2) + nbits - 1
        g = max(0, g)
        xc = (xa * 2**g) // xb
        mc = ma - mb - g

        xc = max(xc, 1)     # Posit never round to 0.
        xc *= sign

        return self._fixedpoint_to_posit(xc, mc, nbits=nbits, es=es)


    def __floordiv__(self, other):
        raise NotImplementedError


    def __eq__(self, other):
        raise NotImplementedError


    def __ne__(self, other):
        raise NotImplementedError


    def __lt__(self, other):
        raise NotImplementedError


    def __le__(self, other):
        raise NotImplementedError


    def __gt__(self, other):
        raise NotImplementedError


    def __ge__(self, other):
        raise NotImplementedError


    def __str__(self):
        return coder.positrep_to_str(self.rep)


    # Return (x,m) representing number = x * 2^m
    def _fixedpoint(self):
        rep = self.rep

        x = (-1)**rep['s'] * (2**rep['h'] + rep['f'])
        m = 2**rep['es'] * rep['k'] + rep['e'] - rep['h']

        return (x,m)


    @classmethod
    def _fixedpoint_to_posit(cls, x, m, nbits=None, es=None):
        assert nbits is not None
        assert es is not None

        if x == 0:
            return PCPosit('0', nbits=nbits, es=es)

        p = PCPosit(nbits=nbits, es=es)
        p.rep['t'] = 'n'
        p.rep['s'] = 0

        if x < 0:
            x = -x
            p.rep['s'] = 1

        assert x != 0

        while x != 0 and x % 2 == 0:
            x >>= 1
            m += 1

        g = 0
        y = x
        while y >= 2:
            y >>= 1
            g -= 1

        assert y >= 1 and y < 2, "y={}".format(y)

        p.rep['e'] = (m - g) % 2**es
        p.rep['k'] = (m - g) // 2**es

        p.rep['h'] = -g
        p.rep['f'] = x - 2**p.rep['h']

        bits = coder.encode_posit_binary(p.rep)
        p.rep = coder.decode_posit_binary(bits, nbits=nbits, es=es)

        return p
