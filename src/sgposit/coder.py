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


import copy
import numbers
import sys

if sys.version_info.major >= 3:
    from math import gcd
else:
    from fractions import gcd

from sgposit import bitops


def create_positrep(nbits=32, es=2, s=0, k=0, e=0, f=0, h=0, t='n'):
    return { 's': s, 'k': k, 'e': e, 'f': f, 'h': h, 'nbits': nbits, 'es': es, 't': t }


def create_zero_positrep(nbits=32, es=2):
    return create_positrep(nbits=nbits, es=es, s=0, k=0, e=0, f=0, h=0, t='z')


def create_cinf_positrep(nbits=32, es=2):
    return create_positrep(nbits=nbits, es=es, s=0, k=0, e=0, f=0, h=0, t='c')


def copy_positrep(rep):
    return copy.deepcopy(rep)


def decode_posit_binary(bits, nbits, es):
    assert nbits >= 2 and es >= 0

    rep = create_positrep(nbits=nbits, es=es)

    if bits == 0:
        rep['t'] = 'z'
        return rep
    elif bits == (1 << (nbits-1)):
        rep['t'] = 'c'
        return rep

    assert rep['t'] == 'n'

    rep['s'] = bitops.get_int_bits(bits, nbits-1)

    if rep['s'] == 1: bits = -bits

    regime = bitops.get_int_bits(bits, nbits-2)
    nleads = bitops.count_leading_bits(bits, regime, nbits-2)

    if regime == 0:
        assert 1 <= nleads and nleads <= nbits-2
        rep['k'] = -nleads
    else:
        assert 1 <= nleads and nleads <= nbits-1
        rep['k'] = nleads - 1

    i = nbits - 1 - nleads - 1 - 1      # n - signbit - rs - rbar - nextbit

    e = 0
    nebits = 0
    while i >= 0 and nebits < es:
        e = 2*e | bitops.get_int_bits(bits, i)
        i -= 1
        nebits += 1
    e <<= es - nebits
    rep['e'] = e

    rep['h'] = max(0, i+1)      # Remaining bits, and +1 since i is 0-based.
    if rep['h'] > 0:
        rep['f'] = bitops.get_int_bits(bits, 0, i)

    return rep


def encode_posit_binary(rep):
    assert isinstance(rep['nbits'], numbers.Integral) and rep['nbits'] >= 2
    assert isinstance(rep['es'   ], numbers.Integral) and rep['es'] >= 0
    assert isinstance(rep['s'    ], numbers.Integral) and (rep['s'] == 0 or rep['s'] == 1)
    assert isinstance(rep['e'    ], numbers.Integral) and rep['e'] >= 0 and rep['e'] <= 2**rep['es'] - 1
    assert isinstance(rep['h'    ], numbers.Integral) and rep['h'] >= 0
    assert isinstance(rep['f'    ], numbers.Integral) and rep['f'] >= 0 and rep['f'] <= 2**rep['h'] - 1
    assert rep['t'] in ['c', 'n', 'z']

    if rep['t'] == 'z':
        return 0
    elif rep['t'] == 'c':
        return 1 << (rep['nbits']-1)

    assert rep['t'] == 'n'

    maxpos_bits = 2**(rep['nbits']-1) - 1

    n = rep['nbits'] - 1    # Remaining number of bits after reserving 1 for sign bit.
    bits = 0
    rounded = False

    if rep['k'] >= 0:
        if n >= rep['k'] + 1:
            bits = bitops.create_mask(rep['k'] + 1)
            n -= rep['k'] + 1

            assert n >= 0

            if n > 0:
                bits <<= 1
                n -= 1
        else:
            bits = bitops.create_mask(n)
            n = 0
            rounded = True
    else:
        bits = 1
        if n < -rep['k'] + 1:
            rounded = True
        n -= min(n, -rep['k'] + 1)

    assert n >= 0

    if n >= rep['es']:
        bits <<= rep['es']
        bits |= rep['e']
        n -= rep['es']
    elif rounded == False:
        assert rep['es'] > 0

        m = rep['es'] - n       # Number of exponent bits to truncate.
        te = rep['e'] >> m
        te <<= m                # Rounded down exponent bits.

        value = rep['e'] * 2**rep['h'] + rep['f']
        represented_value = te * 2**rep['h']
        truncation = value - represented_value
        tie = 2**(m + rep['h'] - 1)

        te >>= m        # Truncated exponent bits.
        bits <<= n
        bits |= te
        n = 0

        if truncation == tie:
            if bits & 0x01 and bits < maxpos_bits:
                bits += 1
        elif truncation > tie:
            if bits < maxpos_bits:
                bits += 1

        rounded = True

    assert n >= 0

    if n > rep['h']:
        bits <<= rep['h']
        bits |= rep['f']
        n -= rep['h']

        bits <<= n
        n = 0

    elif rounded == False:
        m = rep['h'] - n    # Number of fractional bits to truncate.
        tf = rep['f'] >> m
        tf <<= m            # Rounded down fractional bits.

        value = rep['f']
        represented_value = tf
        truncation = value - represented_value
        tie = 2**(m-1)

        tf >>= m    # Truncated fractional bits.
        bits <<= n
        bits |= tf
        n = 0

        if truncation == tie:
            if bits & 0x01 and bits < maxpos_bits:
                bits += 1
        elif truncation > tie:
            if bits < maxpos_bits:
                bits += 1

        rounded = True

    assert n == 0

    if rep['s'] == 1:
        bits = -bits
        mask = bitops.create_mask(rep['nbits'])
        bits &= mask

    assert isinstance(bits, numbers.Integral) and bits >= 0 and bits <= bitops.create_mask(rep['nbits'])

    return bits


def positrep_to_str(rep):
    if rep['t'] == 'z':
        return '0'
    elif rep['t'] == 'c':
        return 'cinf'

    assert rep['t'] == 'n'

    out = ''
    if rep['s'] == 1:
        out = '-'

    E = (2**rep['es'] * rep['k']) + rep['e']
    V = (1 << rep['h']) + rep['f']
    D = rep['h']

    if E >= 0:
        V <<= E
    else:
        D += -E

    mask = bitops.create_mask(D)
    fraction_bits = V & mask
    integral = V >> D

    num = 0
    den = 1
    for d in range(D):
        if fraction_bits & 0x01 == 1:
            num += den
        den *= 2
        fraction_bits >>= 1

    if num == 0:
        out += str(integral)
    else:
        if integral != 0:
            out += str(integral)
            out += '-' if rep['s'] == 1 else '+'
        g = gcd(num, den)
        num //= g
        den //= g
        out += str(num) + '/' + str(den)

    return out


# FIXME: refactor
def positrep_to_rational_str(rep):
    if rep['t'] == 'z':
        return '0'
    elif rep['t'] == 'c':
        return 'cinf'

    assert rep['t'] == 'n'

    out = ''
    if rep['s'] == 1:
        out = '-'

    E = (2**rep['es'] * rep['k']) + rep['e']
    V = (1 << rep['h']) + rep['f']
    D = rep['h']

    if E >= 0:
        V <<= E
    else:
        D += -E

    mask = bitops.create_mask(D)
    fraction_bits = V & mask
    integral = V >> D

    num = 0
    den = 1
    for d in range(D):
        if fraction_bits & 0x01 == 1:
            num += den
        den *= 2
        fraction_bits >>= 1

    if num == 0:
        out += str(integral)
    else:
        num += den*integral
        g = gcd(num, den)
        num //= g
        den //= g
        out += str(num) + '/' + str(den)

    return out
