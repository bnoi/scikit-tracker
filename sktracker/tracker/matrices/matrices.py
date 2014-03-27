import logging
import numpy as np

from ..cost_function import AbstractLinkCostFunction
from ..cost_function import AbstractDiagCostFunction
from ..lapjv import lapjv

log = logging.getLogger(__name__)


class CostMatrix():
    """This class represents the cost matrix which will be given to LAPJV solver.
    Cost matrix is built from matrices blocks.

    Parameters
    ----------
    blocks : 2D list of `numpy.ndarray` or None
        Each array value is a block or None (filled with np.nan).

    """

    def __init__(self, blocks):

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

    def view(self, ax=None, colormap="gray", **kwargs):
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

        col_labels = np.hstack(np.array([list(range(s)) for s in col_shapes.astype(np.int)]))
        row_labels = np.hstack(np.array([list(reversed(range(s))) for s in row_shapes[::-1].astype(np.int)]))

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

    def _fill_lrb(self):
        """Fill the lower contiguous block of NaN values with the transposed
        matrix of the related upper block.
        """

        # Find the lower contiguous block of NaN values
        ii, jj = np.where(np.isfinite(self.mat) is False)
        for i, j in zip(ii, jj):
            if np.isnan(self.mat[i:, j:]).all():
                break
        # Copy the upper left block and transpose
        lrb = self.mat[:i, :j].T.copy()
        # Give a value higher than the max value
        lrb[np.isfinite(lrb)] = self.get_masked().max() + 1.

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
        row_shapes : 1D `numpy.ndarray`
            Row shapes.
        col_shapes : 1D `numpy.ndarray`
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

        return row_shapes, col_shapes


class Block():
    """A matrix block.
    """
    pass


class LinkBlock(Block):
    """LinkBlock are built with two vectors.

    Parameters
    ----------
    objects_in : 1D array of `pandas.DataFrame`
        To fill Y block axis.
    objects_out : 1D array of `pandas.DataFrame`
        To fill X block axis.
    cost_function : `sktracker.tracker.CostFunction`
        Used to compute block costs.

    """

    def __init__(self,
                 objects_in,
                 objects_out,
                 cost_function):

        self.objects_in = objects_in
        self.objects_out = objects_out

        if not isinstance(cost_function, AbstractLinkCostFunction):
            raise TypeError("cost_function needs to inherit from "
                            "sktracker.tracker.cost_function.LinkCostFunction")
        self.cost_function = cost_function
        self.mat = None

        self._build()

    def _build(self):
        """Compute and built block.
        """

        self.mat = self.cost_function.build(self.objects_in, self.objects_out)

        if self.mat.shape != (len(self.objects_in),
                              len(self.objects_out)):
            self.mat = None
            raise ValueError('Cost_function does not returns'
                             ' a correct cost matrix')


class DiagBlock(Block):
    """DiagBlock are built with one single vector. It is an identity matrix.

    Parameters
    ----------
    objects : 1D array of `pandas.DataFrame`
        To fill the identity matrix.
    cost_function : `sktracker.tracker.CostFunction`
        Used to compute block costs.

    """
    def __init__(self, objects, cost_function):

        self.objects = objects

        if not isinstance(cost_function, AbstractDiagCostFunction):
            raise TypeError("cost_function needs to inherit from "
                            "sktracker.tracker.cost_function.DiagCostFunction")

        self.cost_function = cost_function
        self.vect = None
        self.mat = None

    def build(self):
        """Compute and built block.
        """
        self.vect = self.cost_function.build(self.objects)

        if self.vect.size != len(self.objects):
            raise ValueError('cost_function does not returns'
                             ' a correct cost vector')

        self._get_matrix()

    def _get_matrix(self):
        """Get matrix and replace 0 values with `numpy.nan`.
        """

        size = self.vect.shape[0]
        self.mat = np.empty((size, size))
        self.mat[:] = np.nan
        self.mat[np.diag_indices(size)] = self.vect
