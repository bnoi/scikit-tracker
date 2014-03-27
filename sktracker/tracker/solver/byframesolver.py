
import numpy as np

from ..matrices import LinkBlock
from ..matrices import DiagBlock
from ..matrices import CostMatrix

from ..cost_function import AbstractLinkCostFunction
from ..cost_function import AbstractDiagCostFunction

from ...utils.dataframes import relabel_fromzero

class ByFrameSolver:
    """
    """
    def __init__(self, trajs, cost_functions):
        
        self.trajs = trajs.copy()
        self.t_in = 0
        self.t_out = 0
        
        self.link_cf = cost_functions['link']
        if not isinstance(self.link_cf, AbstractLinkCostFunction):
            raise TypeError(''' The cost function {} doesn't '''
                            ''' inherit from AbstractLinkCostFunction'''.format(self.link_cf))
                            
        self.birth_cf = cost_functions['birth']
        if not isinstance(self.birth_cf, AbstractDiagCostFunction):
            raise TypeError(''' The cost function {} doesn't '''
                            ''' inherit from AbstractDiagCostFunction'''.format(self.birth_cf))
                            
        self.death_cf = cost_functions['death']
        if not isinstance(self.death_cf, AbstractDiagCostFunction):
            raise TypeError(''' The cost function {} doesn't '''
                            ''' inherit from AbstractDiagCostFunction'''.format(self.death_cf))
        
        self.max_assigned_cost = self.death_cf.context['cost'] / 1.05
                     
        
    @property
    def blocks_structure(self):
        return [[self.link_block.mat, self.death_block.mat],
                [self.birth_block.mat, None]]
        
    @property
    def pos_in(self):
        return self.trajs.loc[self.t_in]

    @property
    def pos_out(self):
        return self.trajs.loc[self.t_out]

    @property
    def times(self):
        return self.trajs.index.get_level_values('t_stamp').unique()
        
    def track(self):
        """
        """
        old_label = self.trajs.index.get_level_values('label').values
        self.trajs['new_label'] = old_label.astype(np.float)
        ts_in = self.times[:-1]
        ts_out = self.times[1:]
        for t_in, t_out in zip(ts_in, ts_out):
            self._one_frame(t_in, t_out)
        self._relabel_trajs()
        return self.trajs
        
    def _one_frame(self, t_in, t_out):
        
        self.t_in = t_in
        self.t_out = t_out
        pos_in = self.pos_in
        pos_out = self.pos_out
        
        self.link_block = LinkBlock(pos_in, pos_out, self.link_cf)
        self.birth_block = DiagBlock(pos_out, self.birth_cf)
        self.death_block = DiagBlock(pos_in, self.death_cf)
        
        self.cm = CostMatrix(self.blocks_structure)
        self.cm.solve()
        self.assign()
        
    def assign(self):
        
        row_shapes, col_shapes = self.cm.get_shapes()
        last_out_link = row_shapes[0]
        last_in_link = col_shapes[0]
        
        for idx_out, idx_in in enumerate(self.cm.out_links[:last_out_link]):
            if idx_in >= last_in_link:
                # new segment
                new_label = self.trajs['new_label'].max() + 1.
            else:
                # assignment
                new_label = self.trajs.loc[self.t_in]['new_label'].iloc[idx_in]
                self._update_max_assign_cost(self.cm.costs[idx_in])
            self.trajs.loc[self.t_out, 'new_label'].iloc[idx_out] = new_label

    def _update_max_assign_cost(self, cost):
        if cost > self.max_assigned_cost:
            self.max_assigned_cost = cost
            
            ## Update context
            self.birth_cf.context['cost'] = self.max_assigned_cost * 1.05
            self.death_cf.context['cost'] = self.max_assigned_cost * 1.05

    def _relabel_trajs(self):

        self.trajs.set_index('new_label', append=True, inplace=True)
        self.trajs.reset_index(level='label', drop=True, inplace=True)
        self.trajs.index.names = ['t', 'label']
        self.trajs.sortlevel('label', inplace=True)
        self.trajs.sortlevel('t', inplace=True)
        relabel_fromzero(self.trajs, 'label', inplace=True)


