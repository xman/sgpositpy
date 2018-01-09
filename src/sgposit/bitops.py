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


"""
Create a mask with n ones.
"""
def create_mask(n):
    if n <= 0:
        return 0
    return (1 << n) - 1


"""
Get bits in integer v from bit ifirst to bit ilast, inclusive.
Integer v = b_n-1, ..., b_1, b_0
The bit position is 0-based and starts from the least significant bit.
"""
def get_int_bits(v, ifirst, ilast=None):
    if ilast is None: ilast = ifirst

    assert ifirst >= 0 and ifirst <= ilast

    mask = create_mask(ilast-ifirst+1)
    v >>= ifirst
    v &= mask

    return v


"""
Count the number of leading bits with value b, from bit ilast down to bit 0.
Integer v = b_n-1, ..., b_1, b_0
The bit position is 0-based and starts from the least significant bit.
"""
def count_leading_bits(bits, b, ilast):
    assert ilast >= 0

    count = 0
    for i in range(ilast, -1, -1):
        if get_int_bits(bits, i) == b:
            count += 1
        else:
            break

    return count
