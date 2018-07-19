"""
Module containing custom colormaps and transformations

This module contains a set of functions to import, create and alter
Matplotlib colormaps. Colours are specified by red-green-blue-alpha
(RGBA) values from 0 to 1, meaning color transformations can be written
as array operations.

Notes
-----
Custom colormaps are automatically added to the module attributes. See
Custom.populate_maps for a list of custom colormaps.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col


class Custom(object):
    """
    The custom colormaps object.

    Attributes
    ----------
    maps : dict
        Dictionary of custom colormaps.
    """
    def __init__(self):
        self.maps = dict()
        self.populate_maps()

    def populate_maps(self):
        """Populate the list of custom colormaps.

        Notes
        -----
        Adds custom colormaps to the self.maps, which are then
        added to the global namespace of the module.

        Custom colormaps include:
            wiridis
                Reversed viridis blended with white at the start.
        """
        maps = dict(
            wiridis = add_white('viridis_r')
                    )
        for key in maps:
            maps[key].name = key
        self.maps.update(maps)


def import_colormap(cmap):
    """Checks if a cmap is a string or a matplotlib cmap object.

    Parameters
    ----------
    cmap : str or matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap or a string corresponding to a
        default colormap.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Requested matplotlib colormap.
    """
    if isinstance(cmap, str):
        return plt.cm.get_cmap(cmap)
    else:
        return cmap


def rgba_lightness(rgba):
    """Determines the lightness elements of an RGBA list.

    Parameters
    ----------
    rgba : tuple
        Tuple with at least 3 elements for the RGB fractions (4 for
        alpha).

    Returns
    -------
    float
        Lightness value from 0 (black) to 1 (white).

    Notes
    -----
    Based on jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap.
    The lightness is determined using the formula
        l = sqrt(w . rgb^2),
    where w are the RGB weights, (0.299, 0.587, 0.114).
    """
    rgba = np.array(rgba)
    rgb_wgt = [0.299, 0.587, 0.114]
    return np.sqrt(np.dot(rgba[...,:3]**2, rgb_wgt))


def grayscale_colormap(cmap, ncolor=None):
    """Turns cmap into greyscale.

    Parameters
    ----------
    cmap : str or matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap or a string corresponding to a
        default colormap.
    ncolor : int, optional
        Number of colour values in the colormap. If None, defaults
        to number of elements in the colormap.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap converted to grayscale (see rgba_lightness).
    """
    cm = import_colormap(cmap)
    if ncolor is None:
        ncolor = cm.N
    clist = cm(np.linspace(0, 1, ncolor))
    clist[:,:3] = rgba_lightness(clist)[:,np.newaxis]

    return col.LinearSegmentedColormap.from_list('g' + cm.name, clist)


def invert_colormap(cmap, ncolor=None):
    """Inverts colours from a colormap.

    Parameters
    ----------
    cmap : str or matplotlib.colors.LinearSegmentedColormap
        <atplotlib colormap or a string corresponding to a
        default colormap.
    ncolor : int, optional
        Number of colour values in the colormap. If None, defaults
        to number of elements in the colormap.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap with RGB values inverted by
        rgb_new = 1 - rgb_old.
    """
    cm = import_colormap(cmap)
    if ncolor is None:
        ncolor = cm.N
    clist = cm(np.linspace(0, 1, ncolor))
    clist[:,:3] = 1 - clist[:,:3]

    return col.LinearSegmentedColormap.from_list('i' + cm.name, clist)


def add_rgba(cmap, rgba, nblend=28, loc='start', ncolor=None):
    """Blends an RGBA into a given position in the colormap.

    Parameters
    ----------
    cmap : str or matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap or a string corresponding to a
        default colormap.
    rgba : tuple
        RGB-alpha value to be blended into the colormap.
    nblend : int, optional
        Number of steps taken to blend from RGBA value to colormap value(s).
        Default value of 28 is consisten with linear rate of change in
        uniform colormaps (viridis, plasma).
    loc : str or int, optional
        Location of the blended colour. 'start' or 0 blend at the first
        index, 'end' or 1 blend at the last index, 'mid' or 0.5 blend at
        the middle. All other values between 0 and 1 blend at loc * ncolor.
    ncolor : int, optional
        Number of colour values in the colormap. If None, defaults
        to number of elements in the colormap.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap with an RGBA value blended in a desired
        location.
    """
    cm = import_colormap(cmap)
    if ncolor is None:
        ncolor = cm.N
    norig = ncolor - nblend
    clisti = cm(np.linspace(0, 1, norig))
    if loc == 'start' or loc == 0:
        clistn = blend_rgba(rgba, clisti[0], nblend)
        clist = np.vstack((clistn, clisti))
    elif loc == 'end' or loc == 1:
        clistn = blend_rgba(clisti[-1], rgba, nblend)
        clist = np.vstack((clisti, clistn))
    else:
        if loc == 'mid':
            nmid = norig // 2
        elif loc > 0 and loc < 1:
            nmid = round(norig*loc)
        else:
            raise ValueError('unrecognized value for \'loc\': {}'.format(loc))

        nfwd = (nblend + 1) // 2
        nbak = (nblend + 1) // 2 + (nblend + 1) % 2
        clstart = clisti[:nmid]
        clend = clisti[nmid:]
        clmid1 = blend_rgba(clstart[-1], rgba, nbak)
        clmid2 = blend_rgba(rgba, clend[0], nfwd)[1:]
        clist = np.vstack((clstart, clmid1, clmid2, clend))

    return col.LinearSegmentedColormap.from_list('a' + cm.name, clist)


def add_white(cmap, *args, **kwargs):
    """Adds white to the colormap.

    Parameters
    ----------
    cmap : str or matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap or a string corresponding to a
        default colormap.

    Other Parameters
    ----------------
    *args, **kwargs : optional
        See add_rgba for additional options (nblend, loc, ncolor).

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap with white blended in a desired
        location.
    """
    cm = add_rgba(cmap, [1, 1, 1, 1], *args, **kwargs)
    cm.name = 'w' + cm.name[1:]
    return cm


def add_black(cmap, *args, **kwargs):
    """Adds black to the colormap.

    Parameters
    ----------
    cmap : str or matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap or a string corresponding to a
        default colormap.

    Other Parameters
    ----------------
    *args, **kwargs : optional
        See add_rgba for additional options (nblend, loc, ncolor).

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Matplotlib colormap with black blended in a desired
        location.
    """
    cm = add_rgba(cmap, [0, 0, 0, 1], *args, **kwargs)
    cm.name = 'b' + cm.name[1:]
    return cm


def blend_rgba(rgba1, rgba2, npts=256):
    """Blends smoothly from one RGBA value to another.

    Parameters
    ----------
    rgba1 : tuple
        Starting RGBA value for blending.
    rgba2 : tuple
        Ending RGBA value for blending.
    npts : int, optional
        The number of points for blending.

    Returns
    -------
    numpy.ndarray
        An array of RGBA values ranging from rgba1 to rgba2 which can
        be used to sample colours or generate a LinearSegmentedColormap.
    """
    rgbalist = np.array([np.linspace(rgba1[i], rgba2[i], npts) for i in
                         range(4)]).T
    return rgbalist


# add custom colormaps to the local variables
localcustom = Custom()
locals().update(localcustom.maps)
