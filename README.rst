CustomCMap
==========
A package of custom matplotlib colormaps and colormap transformations.

Ryan J. MacDonell, Apr. 2018

Installation
------------
To install, clone the repository and run the setup script.::

    $ git clone https://github.com/ryjmacdonell/customcmap.git
    $ cd customcmap
    $ python setup.py install

Usage
-----
CustomCMap is made to work with `Matplotlib <https://matplotlib.org>`_. A
custom colormap can easily be incorporated into any plotting script. code:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import customcmap as cm

    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    x, y = np.meshgrid(x, y)
    z = np.exp(-4*(x**2 + y**2))

    plt.pcolormesh(x, y, z, cmap=cm.wiridis)
    plt.colorbar()
    plt.show()
