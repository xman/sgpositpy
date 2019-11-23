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
import operator
from math import isnan as float_isnan

from sgposit import coder


class PCPosit(numbers.Real):
    """
    Possibly correct posit number arithmetic.
    """
    def __init__(self, v=None, mode=None, nbits=None, es=None, force=False):
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
            if not nbits_given:
                nbits = v.rep['nbits']
            if not es_given:
                es = v.rep['es']
            env_adjusted = v._resize_env(nbits, es)
            self.rep = coder.copy_positrep(env_adjusted.rep)
            return 
        elif mode == 'bits':
            if isinstance(v, numbers.Integral):
                self.rep = coder.decode_posit_binary(v, nbits=nbits, es=es)
                return
            elif isinstance(v, str):
                raise NotImplementedError('Binary bit string posit conversion is not implemented.')
        elif isinstance(v, str):
            if v in {'cinf'}:
                self.rep = coder.create_cinf_positrep(nbits=nbits, es=es)
            elif v == '0':
                self.rep = coder.create_zero_positrep(nbits=nbits, es=es)
            else:
                raise ValueError('Expect 0 or cinf posit constant from the input string.')

            return
        if force:
            return self._force_to_posit(v)
        raise ValueError('Input is not supported.')


    def __abs__(self):
        p = PCPosit(self)
        if p.rep['t'] == 'n':
            p.rep['s'] = 0
        return p

    def __add__(self, other):
        old_nbits, old_es = self.rep['nbits'], self.rep['es']
        selfm, otherm = self._match_env(self, other)
        if selfm.rep['t'] == 'z':
            return PCPosit(other)
        elif otherm.rep['t'] == 'z':
            return PCPosit(self)
        elif selfm.rep['t'] == 'c' or otherm.rep['t'] == 'c':
            return PCPosit('cinf', nbits=old_nbits, es=old_es)

        assert selfm.rep['t'] == 'n' and other.rep['t'] == 'n'

        (xa,ma) = selfm._fixedpoint()
        (xb,mb) = otherm._fixedpoint()

        m = max(ma, mb)
        xc = xa*2**(m-mb) + xb*2**(m-ma)
        mc = ma + mb - m

        return self._fixedpoint_to_posit(xc, mc, nbits=old_nbits, es=old_es)
    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return PCPosit(other, force=True).__sub__(self)

    def __pos__(self):
        return PCPosit(self)

    def __neg__(self):
        p = PCPosit(self)
        if p.rep['t'] == 'n':
            p.rep['s'] = p.rep['s'] ^ 1
        return p


    def __mul__(self, other):
        old_nbits, old_es = self.rep['nbits'], self.rep['es']
        selfm, otherm = self._match_env(self, other)
        if selfm.rep['t'] == 'c' or otherm.rep['t'] == 'c':
            return PCPosit('cinf', nbits=old_nbits, es=old_es)
        elif selfm.rep['t'] == 'z' or otherm.rep['t'] == 'z':
            return PCPosit('0', nbits=old_nbits, es=old_es)

        assert selfm.rep['t'] == 'n' and otherm.rep['t'] == 'n'

        (xa,ma) = self._fixedpoint()
        (xb,mb) = other._fixedpoint()

        xc = xa * xb
        mc = ma + mb

        return self._fixedpoint_to_posit(xc, mc, nbits=old_nbits, es=old_es)
    __rmul__ = __mul__


    def __rdiv__(self, other):
        return PCPosit(other, force=True).__div__(self)


    def __truediv__(self, other):
        old_nbits, old_es = self.rep['nbits'], self.rep['es']
        selfm, otherm = self._match_env(self, other)
        if selfm.rep['t'] == 'c' or otherm.rep['t'] == 'z':
            return PCPosit('cinf', nbits=old_nbits, es=old_es)
        elif selfm.rep['t'] == 'z' or otherm.rep['t'] == 'c':
            return PCPosit('0', nbits=old_nbits, es=old_es)

        assert selfm.rep['t'] == 'n' and otherm.rep['t'] == 'n'

        (xa,ma) = selfm._fixedpoint()
        (xb,mb) = otherm._fixedpoint()

        nbits, es = selfm.rep['nbits'], selfm.rep['es']
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

        return self._fixedpoint_to_posit(xc, mc, nbits=old_nbits, es=old_es)
    __div__ = __truediv__

    def __mod__(self, other):
        selfm, otherm = self._match_env(self, other)
        #Have yet to figure out the algorithm here!
        return NotImplemented

    def __rmod__(self, other):
        return PCPosit(other, force=True).__mod__(self)

    def __rtruediv__(self, other):
        return PCPosit(other, force=True).__truediv__(self)

    def __floordiv__(self, other):
        selfm, otherm = self._match_env(self, other)
        result = selfm.__truediv__(otherm).__floor__()
        return self._copy_env(result)

    def __rfloordiv__(self, other):
        return PCPosit(other, force=True).__floordiv__(self)

    def __round__(self, ndigits=None):
        if ndigits == None:
            #round to nearest int
            pass
        else:
            #round to
            pass
        #need to figure out algorithm here!
        return NotImplemented

    def __floor__(self):
        '''
        always round towards -inf
        '''
        if self.rep['t'] == 'z':
            return 0
        if self.rep['t'] == 'c':
            raise ValueError('Cannot convert posit cinf to Integral')
        (sign, intpart, num, den) = coder.positrep_normal_to_rational(self.rep)
        if num == 0:
            return sign*intpart
        else:
            if sign == 1:
                #+ve number: leave truncated
                return sign*intpart
            else:
                #-ve number: decrement truncation
                return sign*intpart - 1

    def __ceil__(self):
        #invert, floor, then invert again
        inverse_floor = self.__neg__().__floor__()
        return -inverse_floor

    def __pow__(self, other):
        #This is a difficult algorithm!
        return NotImplemented

    def __rpow__(self, other):
        return PCPosit(other, force=True).__pow__(self)

    def __eq__(self, other):
        selfm, otherm = self._match_env(self, other)
        a = selfm.rep
        b = otherm.rep

        if a['t'] == 'c' or b['t'] == 'c':
            return False

        elif a['t'] == 'z' or b['t'] == 'z':
            if a['t'] == b['t']:
                return True
            else:
                return False

        else:
            assert a['t'] == 'n'
            assert b['t'] == 'n'

            return a == b


    def __ne__(self, other):
        return not(self == other)


    def __lt__(self, other):
        return self._cmp_op(other, operator.lt)


    def __le__(self, other):
        return self._cmp_op(other, operator.le)


    def __gt__(self, other):
        return self._cmp_op(other, operator.gt)


    def __ge__(self, other):
        return self._cmp_op(other, operator.ge)


    def __str__(self):
        return coder.positrep_to_str(self.rep)

    def __repr__(self):
        nbits, es = self.rep['nbits'], self.rep['es']
        bits = coder.encode_posit_binary(self.rep)
        template = "PCPosit({}, mode='bits', nbits={}, es={})"
        return template.format(hex(bits), nbits, es)

    def __int__(self):
        if self.rep['t'] == 'z':
            return 0
        if self.rep['t'] == 'c':
            raise ValueError('Cannot convert posit cinf to int')
        (sign, intpart, _, _) = coder.positrep_normal_to_rational(self.rep)
        return int(sign * intpart)
    __trunc__ = __int__


    def __float__(self):
        if self.rep['t'] == 'z':
            return 0.0
        if self.rep['t'] == 'c':
            return float('nan')
        (sign, intpart, num, den) = coder.positrep_normal_to_rational(self.rep)
        full_numerator = sign * (intpart * den + num)
        #use integers till last step, minimising rounding error with floats
        return float(full_numerator / den)

    @classmethod
    def from_rational(cls, value, nbits=32, es=2):
        raise NotImplementedError
        """
        numerator, denominator = value
        assert isinstance(numerator, int) and isinstance(denominator, int)
        assert denominator > 0
        #overly precise, which makes for a simpler algorithm
        bits_of_prec = ???
        """

    @classmethod
    def from_float(cls, value, nbits=32, es=2):
        assert isinstance(value, float)
        if float_isnan(value):
            return PCPosit('cinf', nbits=nbits, es=es)
        numerator, denominator = value.as_integer_ratio()
        #assert denominator is power of 2
        assert ((denominator - 1) & denominator) == 0
        power_of_2 = 1
        while denominator > 0:
            power_of_2 -= 1
            denominator >>= 1
        fixedpoint = (numerator, power_of_2)
        return cls._fixedpoint_to_posit(*fixedpoint, nbits, es)

    @classmethod
    def from_int(cls, value, nbits=32, es=2):
        assert isinstance(value, int)
        return cls._fixedpoint_to_posit(value, 0, nbits, es)

    def _cmp_op(self, other, op):
        selfm, otherm = self._match_env(self, other)
        a = selfm.rep
        b = otherm.rep

        if a['t'] == 'c' or b['t'] == 'c':
            return False

        (xa,ma) = self._fixedpoint()
        (xb,mb) = other._fixedpoint()

        m = max(ma, mb)
        xa <<= m - mb
        xb <<= m - ma

        return op(xa, xb)

    @classmethod
    def _force_to_posit(cls, value, nbits=None, es=None):
        """
        Attempt to coerce value into a posit
        """
        if isinstance(value, cls):
            if nbits is None and es is None:
                return cls(value)
            return value._resize_env(nbits, es)
        elif isinstance(value, dict):
            new_posit = cls()
            #assert value looks like a valid rep:
            assert set(new_posit.rep) == set(value)
            new_posit.rep = value
            if nbits is None and es is None:
                return new_posit
            else:
                return new_posit._resize_env(nbits, es)
        else:
            raise TypeError(type(value)) from NotImplementedError()

    @classmethod
    def _match_env(cls, *numbers, nbits_min=32, es_min=2):
        """
        Converts args to posits,
        expanded to the biggest posit environment, to
        have equal nbits and es to each other
        """
        assert len(numbers) > 0
        posits = [cls._force_to_posit(number) for number in numbers]
        nbits_es_dif_max = max(
            abs(posit.rep['nbits'] - posit.rep['es'])
            for posit in posits
        )
        nbits_es_dif_max = max(nbits_es_dif_max, nbits_min)
        es_max = max(posit.rep['es'] for posit in posits)
        es_max = max(es_max, es_min)
        nbits_max = nbits_es_dif_max + es_max
        env_matched = tuple(
            posit._resize_env(nbits_max, es_max) for posit in posits
        )
        return env_matched

    def _resize_env(self, nbits=None, es=None):
        if nbits is None:
            nbits = self.rep['nbits']
        if es is None:
            es = self.rep['es']
        if self.rep['t'] == 'c':
            return PCPosit('cinf', nbits=nbits, es=es)
        fixedpoint = self._fixedpoint()
        return PCPosit._fixedpoint_to_posit(*fixedpoint, nbits, es)

    def _copy_env(self, result):
        nbits, es = self.rep['nbits'], self.rep['es']
        return result._resize_env(nbits, es)

    def _fixedpoint(self):
        """
        Return (x,m) representing number = x * 2^m
        """
        rep = self.rep

        assert rep['t'] != 'c'

        if rep['t'] == 'z':
            x = 0
            m = 0
        else:
            assert rep['t'] == 'n'

            x = (-1)**rep['s'] * (2**rep['h'] + rep['f'])
            m = 2**rep['es'] * rep['k'] + rep['e'] - rep['h']

        return (x,m)

    @classmethod
    def _fixedpoint_to_posit(cls, x, m, nbits, es):
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
