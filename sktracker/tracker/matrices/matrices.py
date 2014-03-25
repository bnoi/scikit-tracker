import logging
import numpy as np

log = logging.getLogger(__name__)



class CostMatrix():
    """
    
    """
    def __init__(self, blocks):
        
        self.blocks = blocks
        self._concatenate_blocks()
        self._fill_lrb()
        
    def _fill_lrb(self):
        ### Find the lower contiguous block of NaN values
        ii, jj = np.where(np.isfinite(self.mat) == False)
        for i, j in zip(ii, jj):
            if np.isnan(self.mat[i:, j:]).all():
                break
        ### Copy the upper left block and transpose
        lrb = self.mat[:i, :j].T.copy()
        ### Give a value higher than the max value
        lrb[np.isfinite(lrb)] = self.get_masked().max() + 1.
        
        self.mat[i:, j:] = lrb
        
    def _concatenate_blocks(self):
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
    
    def get_masked(self):
        return np.ma.masked_invalid(self.mat)
    
    def get_flat(self):
        """
        """
        masked = self.get_masked()
        costs = masked.compressed()
        idxs_in, idxs_out = np.where(
            np.logical_not(np.ma.getmask(masked)))
        return idxs_in, idxs_out, costs


class Block():
    pass

class LinkBlock(Block):
    """
    """
    def __init__(self, objects_in,
                 objects_out,
                 cost_function):
        """
        """
        self.objects_in = objects_in
        self.objects_out = objects_out
        self.cost_function = cost_function
        self.mat = None
        
    def build(self):
        self.mat = self.cost_function(self.objects_in,
                                      self.objects_out)
        if self.mat.shape != (len(self.objects_in),
                              len(self.objects_out)):
            raise ValueError('cost_function does not returns'
                             ' a correct cost matrix')
        
class DiagBlock(Block):
    """
    """
    def __init__(self, objects, cost_function):
        
        self.objects = objects
        self.cost_function = cost_function
        self.vect = None
        
    def build(self):
        self.vect = self.cost_function(self.objects)
        if self.vect.size != len(self.objects):
            raise ValueError('cost_function does not returns'
                             ' a correct cost vector')
    def get_matrix(self):
        return self.vect * np.identity(self.vect.size)

    