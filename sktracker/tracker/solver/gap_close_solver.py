# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import logging

log = logging.getLogger(__name__)

from ..matrix import CostMatrix

from ..cost_function import AbstractCostFunction
from ..cost_function.brownian import BrownianGapCloseCostFunction
from ..cost_function.diagonal import DiagonalCostFunction

from . import AbstractSolver

__all__ = []


class GapCloseSolver(AbstractSolver):
    """

    Parameters
    ----------
    trajs : :class:`pandas.DataFrame`
    cost_functions : list of list
    """
    def __init__(self,
                 trajs,
                 cost_functions,
                 maximum_gap,
                 use_t_stamp=True,
                 coords=['x', 'y', 'z']):

        super(self.__class__, self).__init__(trajs)

        log.info('Initiating gap close solver')
        self.coords = coords

        self.trajs.check_trajs_df_structure(index=['t_stamp', 'label'],
                                            columns=['t'] + coords)

        self.link_cf = cost_functions['link']
        self.check_cost_function_type(self.link_cf, AbstractCostFunction)

        self.birth_cf = cost_functions['birth']
        self.check_cost_function_type(self.birth_cf, AbstractCostFunction)

        self.death_cf = cost_functions['death']
        self.check_cost_function_type(self.death_cf, AbstractCostFunction)

        self.maximum_gap = maximum_gap
        self.use_t_stamp = use_t_stamp

    @classmethod
    def for_brownian_motion(cls, trajs,
                            max_speed,
                            maximum_gap,
                            link_percentile=90,
                            use_t_stamp=True,
                            coords=['x', 'y', 'z']):
        """Close gaps found in different trajectories.

        Parameters
        ----------
        trajs : :class:`sktracker.trajectories.Trajectories`
            Trajectories where to close gaps.
        max_speed : float
            Maximum speed of objects in trajectories.
        maximum_gap : float
            Maximum gap size which can be closed.
        link_percentile : float
            TODO
        use_t_stamp : bool
            If True `t_stamp` index will be used when computing maximum gap. If False, column 't'
            will be used.
        coords : list
            Which columns to choose in trajs when computing distances.

        Examples
        --------
        >>> trajs = data.with_gaps_df()
        >>> max_speed = 10.
        >>> maximum_gap = 5
        >>> gc_solver = GapCloseSolver.for_brownian_motion(trajs, max_speed=max_speed,
        >>>                                                maximum_gap=maximum_gap,
        >>>                                                use_t_stamp=True)
        >>> new_trajs = gc_solver.track()
        2014-08-11:INFO:sktracker.tracker.solver.gap_close_solver: Initiating gap close solver
        2014-08-11:INFO:sktracker.tracker.solver.gap_close_solver: Find candidates among 7 segments
        2014-08-11:INFO:sktracker.tracker.solver.gap_close_solver: 6 candidates found
        2014-08-11:INFO:sktracker.tracker.solver.gap_close_solver: Build cost functions
        2014-08-11:INFO:sktracker.tracker.solver.gap_close_solver: Assigning results
        2014-08-11:INFO:sktracker.tracker.solver.gap_close_solver: 4 gap close event processed
        """

        guessed_cost = float(max_speed ** 2)

        diag_context = {'cost': guessed_cost}
        diag_params = {'link_percentile': link_percentile, 'coords': coords}

        link_cost_func = BrownianGapCloseCostFunction(parameters={'max_speed': max_speed,
                                                                  'coords': coords})
        birth_cost_func = DiagonalCostFunction(context=diag_context,
                                               parameters=diag_params)
        death_cost_func = DiagonalCostFunction(context=diag_context,
                                               parameters=diag_params)

        cost_functions = {'link': link_cost_func,
                          'birth': birth_cost_func,
                          'death': death_cost_func}

        return cls(trajs, cost_functions, maximum_gap, use_t_stamp=use_t_stamp, coords=coords)

    @property
    def blocks_structure(self):
        return [[self.link_cf.mat, self.death_cf.mat],
                [self.birth_cf.mat, None]]

    def track(self, progress_bar=False, progress_bar_out=None):
        """For details about link_percentile, see below from
        K. Jaqaman and G. Danuser, Nature Methods, 2008.

            TFA: For track segment ends and starts, the alternative cost (b and d in Fig. 1c) had to
            be comparable in magnitude to the costs of potential assignments, making the rejection
            of gap closing, merging and splitting an accessible alternative. At the same time, the
            alternative cost had to be at the higher end of the range of potential assignment costs,
            so that the algorithm did not fail to close gaps and capture merge and split events. We
            performed empirical tests of the sensitivity of tracking results to variations in the
            alternative cost. We found that in a range 80th – 100th percentile of all potential
            assignment costs the outcome of gap closing, merging and splitting varied negligibly
            (data not shown). We attribute this robustness to the fact that track initiations and
            terminations competed globally, in space and time, with all other potential assignments.
            Thus, the alternative cost was taken as the 90th percentile.
        """

        idxs_in, idxs_out = self._get_candidates()

        if len(idxs_in) > 10000:
            log.warning("Number of segment's candidates is very high."
                        " Tracking can be very slow.")

        self.link_cf.context['trajs'] = self.trajs
        self.link_cf.context['idxs_in'] = idxs_in
        self.link_cf.context['idxs_out'] = idxs_out
        self.birth_cf.context['objects'] = self.trajs.labels
        self.death_cf.context['objects'] = self.trajs.labels

        if not len(idxs_in):
            log.info('No gap needs closing here')
            return self.trajs

        old_labels = self.trajs.index.get_level_values('label').values
        self.trajs['new_label'] = old_labels.astype(np.float)

        log.info('Build cost functions')

        link_percentile_b = self.birth_cf.parameters['link_percentile']
        link_percentile_d = self.death_cf.parameters['link_percentile']
        self.link_cf.get_block()
        link_costs = np.ma.masked_invalid(self.link_cf.mat).compressed()

        if not link_costs.shape[0]:
            log.info('No suitable gap to fill')
            return self.trajs

        cost_b = np.percentile(link_costs, link_percentile_b)
        cost_d = np.percentile(link_costs, link_percentile_d)
        self.birth_cf.context['cost'] = cost_b
        self.birth_cf.get_block()
        self.death_cf.context['cost'] = cost_d
        self.death_cf.get_block()

        self.cm = CostMatrix(self.blocks_structure)
        self.cm.solve()
        self.assign()

        return self.trajs

    def _get_candidates(self):
        """Find candidate pair of segments for gap closing.
        """
        seg_idx = self.trajs.segment_idxs

        log.info('Find candidates among {} segments'.format(len(seg_idx)))

        max_gap = self.maximum_gap
        labels = self.trajs.labels

        if self.use_t_stamp:
            bounds = self.trajs.get_bounds()
        else:
            bounds = self.trajs.get_bounds(column='t')

        bounds = np.array(list(bounds.values()))

        start_times = bounds[:, 0]
        stop_times = bounds[:, 1]
        ss_in, ss_out = np.meshgrid(labels, labels)

        gaps_size = start_times[ss_out] - stop_times[ss_in]

        matches = np.argwhere((gaps_size > 0) * (gaps_size <= max_gap))

        if not matches.shape[0]:
            log.info("No candidate found")
            return [], []

        matches_in = matches[:, 1]
        matches_out = matches[:, 0]

        if not self.use_t_stamp:
            start_times = self.trajs.get_t_stamps_correspondences(start_times, column='t')
            stop_times = self.trajs.get_t_stamps_correspondences(stop_times, column='t')

        in_idxs = np.column_stack([stop_times, self.trajs.labels])
        in_idxs = in_idxs[matches_in]
        out_idxs = np.column_stack([start_times, self.trajs.labels])
        out_idxs = out_idxs[matches_out]

        # Convert idx in list of tuple
        # Otherwise trajs.loc[] indexing fails.
        # See https://github.com/pydata/pandas/issues/7981
        in_idxs = [tuple(v) for v in in_idxs]
        out_idxs = [tuple(v) for v in out_idxs]

        log.info("{} candidates found".format(len(in_idxs)))

        return in_idxs, out_idxs

    def assign(self):
        """
        """
        log.info('Assigning results')

        row_shapes, col_shapes = self.cm.get_shapes()
        old_labels = self.trajs.index.get_level_values(level='label').values
        new_labels = old_labels.copy()
        unique_old = self.trajs.labels.copy()  # np.unique(old_labels)
        unique_new = self.trajs.labels.copy()  # np.unique(new_labels)

        last_in_link = row_shapes[0]
        last_out_link = col_shapes[0]

        n = 0
        for idx_out, idx_in in enumerate(self.cm.out_links[:last_out_link]):
            if idx_in >= last_in_link:
                # no merge
                unique_new[idx_out] = unique_new.max() + 1
            else:
                # do merge
                new_label = unique_new[idx_in]
                unique_new[idx_out] = new_label
                n += 1

        for old, new in zip(unique_old, unique_new):
            new_labels[old_labels == old] = new

        log.info("{} gap close event processed".format(n))
        self.relabel_trajs(new_labels)
        return self.trajs
