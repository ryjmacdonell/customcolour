"""
Script for plotting the different colormap types.
"""
import numpy as np
import matplotlib.pyplot as plt
import customcolour.cmap as cm


def main():
    """Tests for different colormap generation and tranformation.

    Based on matplotlib.org/examples/color/colormaps_reference.html.
    """
    cmaps = [
        cm.wiridis,
        cm.grayscale_colormap(cm.wiridis),
        cm.grayscale_colormap('jet'),
        cm.invert_colormap('jet'),
        cm.add_black('jet'),
        cm.add_black('jet', loc='end'),
        cm.add_white('jet', loc='mid'),
        cm.add_white('jet', loc=0.2),
        cm.add_rgba('jet', [1, 1, 0, 1], loc=0.02),
        cm.add_rgba('jet', [1, 0, 1, 1], nblend=32),
        cm.add_rgba('jet', [1, 1, 1, 1], ncolor=32)
             ]

    ncmap = len(cmaps)
    grad = np.vstack((np.linspace(0, 1, 256), np.linspace(0, 1, 256)))
    fig, axarr = plt.subplots(nrows=ncmap)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    for ax, c in zip(axarr, cmaps):
        ax.imshow(grad, aspect='auto', cmap=c)
        pos = list(ax.get_position().bounds)
        xtxt = pos[0] - 0.01
        ytxt = pos[1] + pos[3]/2.
        fig.text(xtxt, ytxt, c.name, va='center', ha='right', fontsize=10)
        ax.set_axis_off()

    plt.show()


if __name__ == '__main__':
    main()
