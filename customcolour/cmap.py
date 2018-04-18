"""
Module containing custom colormaps and transformations
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


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


def invert_colormap(cmap, ncolor=256):
    """Invert colours from a colormap."""
    cm = import_colormap(cmap)
    clist = cm(np.linspace(0, 1, ncolor))
    clist[:,:3] = 1 - clist[:,:3]

    return LinearSegmentedColormap.from_list('i' + cm.name, clist)


def add_rgba(cmap, rgba, nblend=16, loc='start', ncolor=256):
    """Blend an RGBA into a given position in the colormap."""
    cm = import_colormap(cmap)
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
        resfwd = nmid + nfwd - norig
        resbak = nbak - nmid
        if resfwd > 0:
            nfwd -= resfwd
            nbak += resfwd
        elif resbak > 0:
            nfwd += resbak
            nbak -= resbak
        clstart = clisti[:nmid]
        clend = clisti[nmid:]
        clmid1 = blend_rgba(clstart[-1], rgba, nbak)
        clmid2 = blend_rgba(rgba, clend[0], nfwd)[1:]
        clist = np.vstack((clstart, clmid1, clmid2, clend))

    return colors.LinearSegmentedColormap.from_list('a' + cm.name, clist)


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
