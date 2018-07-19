"""
Module containing custom colormaps and transformations
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col


class Custom(object):
    """
    The custom colormaps object.
    """
    def __init__(self):
        self.maps = dict()
        self.populate_maps()

    def populate_maps(self):
        """Populate the list of custom colormaps."""
        maps = dict(
            wiridis = add_white('viridis_r')
                    )
        for key in maps:
            maps[key].name = key
        self.maps.update(maps)


def import_colormap(cmap):
    """Checks if a cmap is a string or a matplotlib cmap object."""
    if isinstance(cmap, str):
        return plt.cm.get_cmap(cmap)
    else:
        return cmap


def rgba_lightness(rgba):
    """Determines the lightness elements of an RGBA list.

    Based on jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap
    """
    rgba = np.array(rgba)
    rgb_wgt = [0.299, 0.587, 0.114]
    return np.sqrt(np.dot(rgba[...,:3]**2, rgb_wgt))


def grayscale_colormap(cmap, ncolor=None):
    """Turns cmap into greyscale."""
    cm = import_colormap(cmap)
    if ncolor is None:
        ncolor = cm.N
    clist = cm(np.linspace(0, 1, ncolor))
    clist[:,:3] = rgba_lightness(clist)[:,np.newaxis]

    return col.LinearSegmentedColormap.from_list('g' + cm.name, clist)


def invert_colormap(cmap, ncolor=None):
    """Invert colours from a colormap."""
    cm = import_colormap(cmap)
    if ncolor is None:
        ncolor = cm.N
    clist = cm(np.linspace(0, 1, ncolor))
    clist[:,:3] = 1 - clist[:,:3]

    return col.LinearSegmentedColormap.from_list('i' + cm.name, clist)


def add_rgba(cmap, rgba, nblend=28, loc='start', ncolor=None):
    """Blend an RGBA into a given position in the colormap.

    Default value of nblend is consistent with rate of change in lightness
    of matplotlib uniform colormaps (viridis, plasma).
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
    """Add white to the colormap."""
    cm = add_rgba(cmap, [1, 1, 1, 1], *args, **kwargs)
    cm.name = 'w' + cm.name[1:]
    return cm


def add_black(cmap, *args, **kwargs):
    """Add white to the colormap."""
    cm = add_rgba(cmap, [0, 0, 0, 1], *args, **kwargs)
    cm.name = 'b' + cm.name[1:]
    return cm


def blend_rgba(rgba1, rgba2, npts):
    """Blend smoothly from one RGBA value to another."""
    rgbalist = np.array([np.linspace(rgba1[i], rgba2[i], npts) for i in
                         range(4)]).T
    return rgbalist


# add custom colormaps to the local variables
localcustom = Custom()
locals().update(localcustom.maps)
