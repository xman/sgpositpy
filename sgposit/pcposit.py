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

from sgposit import coder


"""
Provably correct posit number arithmetic.
"""
class PCPosit:

    def __init__(self, v=None, mode=None, nbits=None, es=None):
        if v is None:
            self.rep = coder.create_positrep(nbits=nbits, es=es, t='z')
            return
        elif isinstance(v, PCPosit):
            if nbits is not None and v.rep['nbits'] != nbits:
                    raise NotImplementedError('Mismatched nbits posit conversion is not implemented.')
            if es is not None and v.rep['es'] != es:
                    raise NotImplementedError('Mismatched es posit conversion is not implemented.')
            self.rep = copy.deepcopy(v.rep)
            return
        elif mode == 'bits':
            if isinstance(v, int):
                self.rep = coder.decode_posit_binary(v, nbits=nbits, es=es)
                return
            elif isinstance(v, str):
                raise NotImplementedError('Binary bit string posit conversion is not implemented.')

        raise ValueError('Input is not supported.')


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
