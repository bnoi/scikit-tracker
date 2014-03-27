
import numpy as np

from ..matrices import LinkBlock
from ..matrices import DiagBlock
from ..matrices import CostMatrix

from ..cost_function import AbstractLinkCostFunction
from ..cost_function import AbstractDiagCostFunction

from ..cost_function import BrownianCostFunction
from ..cost_function import DiagCostFunction


from . import AbstractSolver


class ByFrameSolver(AbstractSolver):
    """

    Parameters
    ----------
    trajs : pandas.DataFrame
    cost_functions : list of list
    """
    def __init__(self, trajs, cost_functions, coords=['x', 'y', 'z']):

        super().__init__(trajs)

        self.t_in = 0
        self.t_out = 0

        self.coords = coords

        self.check_trajs_df_structure(index=['t_stamp', 'label'], columns=['t'] + coords)

        self.link_cf = cost_functions['link']
        self.check_cost_function_type(self.link_cf, AbstractLinkCostFunction)

        self.birth_cf = cost_functions['birth']
        self.check_cost_function_type(self.birth_cf, AbstractDiagCostFunction)

        self.death_cf = cost_functions['death']
        self.check_cost_function_type(self.death_cf, AbstractDiagCostFunction)

        self.max_assigned_cost = self.death_cf.context['cost'] / 1.05

    @classmethod
    def for_brownian_motion(cls, trajs, max_speed, coords=['x', 'y', 'z']):
        """

        Parameters
        ----------
        trajs : pandas.DataFrame
        max_speed : float
            Max objects velocity
        coords : list
        """

        guessed_cost = max_speed ** 2
        cost_functions = {'link': BrownianCostFunction({'max_speed': max_speed,
                                                        'coords': coords}),
                          'birth': DiagCostFunction({'cost': guessed_cost}),
                          'death': DiagCostFunction({'cost': guessed_cost})}

        return cls(trajs, cost_functions, coords=coords)

    @property
    def blocks_structure(self):
        return [[self.link_block.mat, self.death_block.mat],
                [self.birth_block.mat, None]]

    def track(self):
        """

        Returns
        -------
        self.trajs : pandas.DataFrame
        """
        old_label = self.trajs.index.get_level_values('label').values
        self.trajs['new_label'] = old_label.astype(np.float)
        ts_in = self.times[:-1]
        ts_out = self.times[1:]

        for t_in, t_out in zip(ts_in, ts_out):
            self.one_frame(t_in, t_out)
        self.relabel_trajs()

        return self.trajs

    def one_frame(self, t_in, t_out):
        """

        Parameters
        ----------
        t_in : int
        t_out : int
        """

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
        """
        """

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
                self._update_max_assign_cost(self.cm.mat[idx_in, idx_out])
            self.trajs.loc[self.t_out, 'new_label'].iloc[idx_out] = new_label

    def _update_max_assign_cost(self, cost):
        if cost > self.max_assigned_cost:
            self.max_assigned_cost = cost

            self.birth_cf.context['cost'] = self.max_assigned_cost * 1.05
            self.death_cf.context['cost'] = self.max_assigned_cost * 1.05
