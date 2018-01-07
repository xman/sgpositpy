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


class PCPosit:

    def __init__(self, v, nbits=32, es=2):
        self.nbits = nbits
        self.es = es
        self.u = 2**(2**es)


    def __add__(self, other):
        raise NotImplementedError


    def __sub__(self, other):
        raise NotImplementedError


    def __neg__(self):
        raise NotImplementedError


    def __mul__(self, other):
        raise NotImplementedError


    def __truediv__(self, other):
        raise NotImplementedError


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
        raise NotImplementedError


    def __repr__(self):
        raise NotImplementedError
