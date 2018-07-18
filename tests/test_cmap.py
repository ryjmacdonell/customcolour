"""
Tests for the different customcolour functions
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
import customcolour.cmap as cm


def test_import_colormap_from_string():
    cmap1 = plt.cm.get_cmap('jet')
    cmap2 = cm.import_cmap('jet')
    assert cmap1 == cmap2


def test_import_colormap_from_colormap():
    cmap1 = plt.cm.get_cmap('jet')
    cmap2 = cm.import_cmap(cmap1)
    assert cmap1 == cmap2


def test_rgba_white_lightness():
    white = (1.0, 1.0, 1.0, 1.0)
    lightness = cm.rgba_lightness(white)
    assert lightness > 1 - 1e-10


def test_rbga_black_lightness():
    black = (0.0, 0.0, 0.0, 1.0)
    lightness = cm.rgba_lightness(black)
    assert lightness < 1e-10


def test_rgba_red_lightness():
    red = (1.0, 0.0, 0.0, 1.0)
    lightness = cm.rgba_lightness(red)
    assert abs(lightness - np.sqrt(0.299)) < 1e-10


def test_grayscale_color():
    cmap1 = cm.import_colormap('jet')
    cmap2 = cm.grayscale_colormap(cmap1)
    c1 = rgba_lightness(cmap1(cmap1.N // 2))
    c2 = cmap2(cmap2.N // 2)
    assert col.same_color(c1, c2)


def test_grayscale_name():
    cmap = cm.grayscale_colormap('jet')
    assert cmap.name = 'gjet'


def test_invert_color():
    cmap1 = cm.import_colormap('jet')
    cmap2 = cm.invert_colormap(cmap1)
    c1 = 1 - np.array(cmap1(0))
    c2 = np.array(cmap2(0))
    assert col.same_color(c1, c2)


def test_add_black_to_start():
    cmap = cm.add_black('jet')
    assert col.same_color(cmap(0), 'k')


def test_add_black_to_end():
    cmap = cm.add_black('jet', loc='end')
    assert col.same_color(cmap(cmap.N), 'k')


def test_add_black_to_mid():
    cmap = cm.add_black('jet', loc='mid')
    assert col.same_color(cmap(cmap.N // 2), 'k')


def test_add_white_to_start():
    cmap = cm.add_white('jet')
    assert col.same_color(cmap(0), 'w')


def test_wiridis_start():
    cmap = cm.wiridis
    assert col.same_color(cmap(0), 'w')


def test_wiridis_end():
    cmap = cm.wiridis
    end_colour = (0.267004, 0.004874, 0.329415, 1.0)
    assert col.same_color(cmap(cmap.N), end_colour)
