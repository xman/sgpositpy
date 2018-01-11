sgpositpy
=========

.. image:: https://badges.gitter.im/sgpositpy/Lobby.svg
   :alt: Join the chat at https://gitter.im/sgpositpy/Lobby
   :target: https://gitter.im/sgpositpy/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. image:: https://travis-ci.org/xman/sgpositpy.svg?branch=master
   :alt: sgpositpy regression test status on Travis CI
   :target: https://travis-ci.org/xman/sgpositpy

.. image:: https://ci.appveyor.com/api/projects/status/3t1q732w1cf4somj/branch/master?svg=true
   :alt: sgpositpy regression test status on Appveyor
   :target: https://ci.appveyor.com/project/xman/sgpositpy

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :alt: sgpositpy under MIT license
   :target: https://github.com/xman/sgpositpy/blob/master/LICENSE

Posit is a new binary format for representing decimal numbers, an alternative to
IEEE 754 floating-point number. Different configurations on the number bit size
and the scaling are possible. Details can be found at the posithub_ and the
`notebook on posit`_.

We are interested to experiment with different posit configurations the `nbits`
and the `es` sizes, and attempt to use smaller bit sizes in our applications
while achieving the required accuracy to operate. However, an implementation
conforming to the posit design is still lacking for popular programming
languages.

This project, *sgpositpy*, is our attempt to develop a prototype implementation
that is correct by the posit design. This can then serve as a reference for
subsequent development of performance optimized posit library. Hence, the
computation efficiency is currently not the focus of the project.

.. _posithub: https://posithub.org
.. _notebook on posit: https://posithub.org/docs/Posits4.pdf


Current status
==============
The current implementation is research oriented and experimental at pre-alpha stage.
This is **NOT** currently suitable for production use.


Install
=======
Install from PyPI

.. code:: bash

    $ pip install sgposit


Install from code repository

.. code:: bash

    $ git clone https://github.com/xman/sgpositpy
    $ cd sgpositpy
    $ pip install -r requirements.txt
    $ python setup.py install

    # Run regression tests.
    $ python setup.py test

    # Enable long running tests.
    $ SGPOSIT_LONG_TESTS=1 python setup.py test


Getting started
===============
The `PCPosit` class is our reference implementation with extensive regression
tests. We shall have performance optimized version in `Posit` class for general
use in the future.

The following code snippet creates posit objects from the given bit patterns,
and the posit configuration, `nbits` and `es`.

.. code:: python

    # file: samples/pcposit_sample.py

    from sgposit.pcposit import PCPosit

    a = PCPosit(0x0C, mode='bits', nbits=6, es=2)
    b = PCPosit(0x0F, mode='bits', nbits=6, es=2)

    c = a + b
    print("{} + {} => {}".format(a, b, c))

    d = a - b
    print("{} - {} => {}".format(a, b, d))

    e = a * b
    print("{} * {} => {}".format(a, b, e))

    f = a / b
    print("{} + {} => {}".format(a, b, f))

    g = -a
    print("uminus {} => {}".format(a, g))


.. code:: bash

    $ python samples/pcposit_sample.py
    1/4 + 3/4 => 1
    1/4 - 3/4 => -1/2
    1/4 * 3/4 => 3/16
    1/4 / 3/4 => 3/8
    uminus 1/4 => -1/4


License
=======
*sgpositpy* is licensed under MIT License.
