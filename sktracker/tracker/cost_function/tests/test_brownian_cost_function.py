import numpy as np
from numpy.testing import assert_array_almost_equal

from sktracker import data

from sktracker.tracker.cost_function.brownian import BrownianLinkCostFunction
from sktracker.tracker.cost_function.brownian import BrownianGapCloseCostFunction


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

    block = cost_func.get_block()

    true_block = [[np.nan, np.nan, 1.551135510361437, np.nan, np.nan],
                  [np.nan, np.nan, np.nan, np.nan, 4.092519418118163],
                  [np.nan, np.nan, np.nan, 0.6004135878472862, np.nan],
                  [np.nan, 2.1081358741648697, np.nan, np.nan, np.nan],
                  [4.033127275182495, np.nan, np.nan, np.nan, np.nan]]

    assert_array_almost_equal(block, true_block)


def test_brownian_gap_close():

    cost_func = BrownianGapCloseCostFunction(parameters={'max_speed': 5.})
