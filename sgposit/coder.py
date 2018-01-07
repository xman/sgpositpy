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


from sgposit import bitops


def decode_posit_binary(bits, nbits, es):
    assert nbits >= 2 and es >= 0

    rep = { 's': 0, 'k': 0, 'e': 0, 'f': 0, 'h': 0, 'nbits': nbits, 'es': es, 't': 'n' }

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
