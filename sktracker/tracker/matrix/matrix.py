# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import logging
import numpy as np

from ..lapjv import lapjv

log = logging.getLogger(__name__)

__all__ = []


class CostMatrix(object):
    """This class represents the cost matrix which will be given to LAPJV solver.
    Cost matrix is built from matrices blocks.

    Parameters
    ----------
    blocks : 2D list of :class:`numpy.ndarray` or None
        Each array value is a block or None (filled with np.nan).
    """

    def __init__(self, blocks):
        """
        """

        if isinstance(blocks, list):
            self.blocks = np.atleast_2d(blocks)
        else:
            self.blocks = blocks

        self._concatenate_blocks()
        self._fill_lrb()

        self.in_links = None
        self.out_links = None
        self.assigned_costs = None

    def solve(self):
        """Solves the linear assignement problem on `self.mat`.
        """

        idxs_in, idxs_out, self.costs = self.get_flat()
        self.in_links, self.out_links = lapjv(idxs_in, idxs_out, self.costs)

    def get_masked(self):
        """Get masked array.

        Returns
        -------
        mat : `numpy.ndarray`
            A masked array on `numpy.nan` of the cost matrix.
        """
        return np.ma.masked_invalid(self.mat)

    def get_flat(self):
        """Get flat vectors according to the cost matrix.

        Returns
        -------
        idxs_in : 1D `numpy.ndarray`
            Y axis indexes.
        idxs_out : 1D `numpy.ndarray`
            X axis indexes.
        costs : 1D `numpy.ndarray`
            Associated costs (matrix value).
        """
        masked = self.get_masked()
        costs = masked.compressed()
        idxs_in, idxs_out = np.where(
            np.logical_not(np.ma.getmask(masked)))
        return idxs_in, idxs_out, costs

    def _fill_lrb(self):
        """Fill the lower contiguous block of NaN values with the transposed
        matrix of the related upper block.
        """

        # Find the lower contiguous block
        x, y = self.get_shapes()
        i = np.sum(x[:len(x) / 2])
        j = np.sum(y[:len(y) / 2])

        # Copy the upper left block and transpose
        lrb = self.mat[:i, :j].T.copy()

        # Give a value higher than the max value
        lrb[np.isfinite(lrb)] = self.get_masked().max() * 1.1

        self.mat[i:, j:] = lrb

    def _concatenate_blocks(self):
        """Concatenate a matrix of block to a single matrix : the cost matrix.
        """

        row_shapes, col_shapes = self.get_shapes()

        nrows = row_shapes.sum()
        ncols = col_shapes.sum()
        self.mat = np.empty((nrows, ncols))
        self.mat.fill(np.nan)

        row_corners = row_shapes.cumsum() - row_shapes
        col_corners = col_shapes.cumsum() - col_shapes

        for i, (start_i, shape_i) in enumerate(zip(row_corners, row_shapes)):
            for j, (start_j, shape_j) in enumerate(zip(col_corners, col_shapes)):
                self.mat[start_i:start_i+shape_i,
                         start_j:start_j+shape_j] = self.blocks[i, j]

    def get_shapes(self):
        """Get whole matrix blocks shape.

        Returns
        -------
        row_shapes : 1D :class:`numpy.ndarray`
            Row shapes.
        col_shapes : 1D :class:`numpy.ndarray`
            Column shapes.
        """
        row_shapes = np.zeros(self.blocks.shape[0])
        col_shapes = np.zeros(self.blocks.shape[1])

        for n, row in enumerate(self.blocks):
            shapes = []
            for block in row:
                if isinstance(block, np.ndarray):
                    shapes.append(block.shape[0])
            if np.unique(shapes).size != 1:
                raise ValueError("Blocks don't fit horizontally")
            row_shapes[n] = shapes[0]

        for n, col in enumerate(self.blocks.T):
            shapes = []
            for block in col:
                if isinstance(block, np.ndarray):
                    shapes.append(block.shape[1])
            if np.unique(shapes).size != 1:
                raise ValueError("Blocks don't fit vertically")
            col_shapes[n] = shapes[0]

        return row_shapes.astype(np.int), col_shapes.astype(np.int)

    def view(self, ax=None, colormap="gray", **kwargs):  # pragma: no cover
        """Display cost matrice on a plot.

        Parameters
        ----------
        colormap : string
            Matplotlib colormap to use. See
            (http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps).
        """

        import matplotlib.pyplot as plt

        if ax:
            fig = ax.get_figure()
        else:
            fig, ax = plt.subplots()

        rec_shape = np.array(self.mat.shape)
        size = rec_shape[0]
        row_shapes, col_shapes = self.get_shapes()

        # Show matrix
        cax = ax.imshow(self.mat, interpolation='none', cmap=colormap,
                        extent=[0, size, 0, size], **kwargs)
        fig.colorbar(cax)

        ax.grid(False)

        # Minor axis
        for i in range(1, size):
            ax.axvline(x=i, ymin=0, ymax=size, linewidth=1, color='black',
                       alpha=0.7)
            ax.axhline(y=i, xmin=0, xmax=size, linewidth=1, color='black',
                       alpha=0.7)

        # Add labels
        ax.set_xticks(np.arange(0.5, size + 0.5))
        ax.set_yticks(np.arange(0.5, size + 0.5))

        col_labels = np.hstack(np.array([list(range(s))
                                         for s in col_shapes.astype(np.int)]))
        row_labels = np.hstack(np.array([list(reversed(range(s)))
                                         for s in row_shapes[::-1].astype(np.int)]))

        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)

        ax.xaxis.tick_top()

        # Add major axis
        for col_id, row_id in zip(np.cumsum(col_shapes), np.cumsum(row_shapes)):
            ax.axvline(x=col_id, ymin=0, ymax=size, linewidth=3, color='black')
            ax.axhline(y=size - row_id, xmin=0, xmax=size, linewidth=3, color='black')

        # Display nan value
        for p in np.argwhere(np.isnan(self.mat)):
            x = p[1] + 0.5
            y = size - 1 - p[0] + 0.5
            ax.scatter(x, y, marker='x', s=500, color='red', alpha=0.3)

        # Show LAPJV solutions
        if self.out_links is not None:
            for idx_out, idx_in in enumerate(self.out_links):
                ax.scatter(idx_out + 0.5, size - 1 - idx_in + 0.5, marker='o',
                           s=500, color='green', alpha=0.4)

        ax.set_xlim(0, size)
        ax.set_ylim(0, size)

        return ax
