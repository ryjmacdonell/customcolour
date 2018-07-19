.. image:: https://travis-ci.org/ryjmacdonell/customcolour.svg?branch=master
    :target: https://travis-ci.org/ryjmacdonell/customcolour

.. image:: https://readthedocs.org/projects/customcolour/badge/?version=latest
    :target: https://customcolour.readthedocs.io/en/latest/?badge=latest

.. image:: https://codecov.io/gh/ryjmacdonell/customcolour/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ryjmacdonell/customcolour

CustomColour
============
A package of custom matplotlib colour tools and transformations.

Ryan J. MacDonell, Apr. 2018

Installation
------------
To install, clone the repository and run the setup script.::

    $ git clone https://github.com/ryjmacdonell/customcolour.git
    $ cd customcolour
    $ python setup.py install

Usage
-----
CustomColour is made to work with `Matplotlib <https://matplotlib.org>`_. A
custom colormap can easily be incorporated into any plotting script::

    import numpy as np
    import matplotlib.pyplot as plt
    import customcolour.cmap as cm

    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    x, y = np.meshgrid(x, y)
    z = np.exp(-4*(x**2 + y**2))

    plt.pcolormesh(x, y, z, cmap=cm.wiridis)
    plt.colorbar()
    plt.show()
