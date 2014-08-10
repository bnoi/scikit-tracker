# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
from numpy.testing import assert_array_almost_equal

from sktracker import data

from sktracker.tracker.cost_function.brownian import BrownianLinkCostFunction
from sktracker.tracker.cost_function.brownian import BrownianGapCloseCostFunction
from sktracker.trajectories import Trajectories


def test_brownian_link():

    trajs = data.brownian_trajs_df()
    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t0 = times_stamp[0]
    t1 = times_stamp[1]
    pos0 = trajs.ix[t0]
    pos1 = trajs.ix[t1]

    cost_func = BrownianLinkCostFunction(parameters={'max_speed': 5.})
    cost_func.context['pos_in'] = pos0
    cost_func.context['pos_out'] = pos1

    cost_func.get_block()
    true_block = [[np.nan, np.nan, 1.551135510361437, np.nan, np.nan],
                  [np.nan, np.nan, np.nan, np.nan, 4.092519418118163],
                  [np.nan, np.nan, np.nan, 0.6004135878472862, np.nan],
                  [np.nan, 2.1081358741648697, np.nan, np.nan, np.nan],
                  [4.033127275182495, np.nan, np.nan, np.nan, np.nan]]

    assert_array_almost_equal(cost_func.mat, true_block)


def test_brownian_gap_close():

    trajs = Trajectories(data.with_gaps_df())
    max_speed = 10.

    cost_func = BrownianGapCloseCostFunction(parameters={'max_speed': max_speed})

    in_idxs = [(3, 0), (3, 0), (5, 1), (13, 2), (13, 2), (16, 3)]
    out_idxs = [(5, 3), (7, 4), (7, 4), (15, 5), (18, 6), (18, 6)]

    cost_func.context['trajs'] = trajs
    cost_func.context['idxs_in'] = in_idxs
    cost_func.context['idxs_out'] = out_idxs

    cost_func.get_block()
    m = cost_func.mat

    m_true = [[np.nan, np.nan, np.nan, 2.0553543815820543, 45.74823093541038, np.nan, np.nan],
              [np.nan, np.nan, np.nan, np.nan, 1.1530875267623917, np.nan, np.nan],
              [np.nan, np.nan, np.nan, np.nan, np.nan, 0.8254178191605767, 23.84513283483594],
              [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 4.916599888362159],
              [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
              [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
              [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]

    assert_array_almost_equal(m, m_true)
