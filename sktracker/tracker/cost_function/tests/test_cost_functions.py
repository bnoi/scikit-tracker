import numpy as np
from numpy.testing import assert_array_almost_equal

from sktracker import data
from sktracker.tracker.matrices import LinkBlock
from sktracker.tracker.matrices import DiagBlock
from sktracker.tracker.matrices import CostMatrix

from sktracker.tracker.cost_function import BrownianCostFunction
from sktracker.tracker.cost_function import DiagCostFunction


def test_brownian_case():

    trajs = data.brownian_trajs_df()
    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t0 = times_stamp[0]
    t1 = times_stamp[1]
    pos0 = trajs.ix[t0]
    pos1 = trajs.ix[t1]

    link_cost_func = BrownianCostFunction({'max_speed': 5.})
    diag_cost_func = DiagCostFunction({'cost':10.})

    link_block = LinkBlock(pos0, pos1, link_cost_func)
    death_block = DiagBlock(pos0, diag_cost_func)
    birth_block = DiagBlock(pos1, diag_cost_func)

    link_block.build()
    death_block.build()
    birth_block.build()

    cost_matrix_structure = [[link_block.mat, death_block.mat],
                             [birth_block.mat, None]]

    cm = CostMatrix(cost_matrix_structure)

    a = np.array([1.55113551, 10., 4.09251942, 10.,
                  0.60041359, 10., 2.10813587, 10.,
                  4.03312728, 10., 10., 11.,
                  10., 11., 10., 11.,
                  10., 11., 10., 11.])
    b = np.ma.masked_invalid(cm.mat).compressed()
    assert_array_almost_equal(a, b, decimal=3)

