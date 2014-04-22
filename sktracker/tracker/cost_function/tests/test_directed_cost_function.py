
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from nose.tools import assert_raises

from sktracker import data

from sktracker.tracker.cost_function.directed import BasicDirectedLinkCostFunction

def test_basic_directed_motion():

    parameters = {'max_speed': 1.,
                  'past_traj_time': 2,
                  'smooth_factor': 0,
                  'interpolation_order': 1,
                  'coords': ['x', 'y', 'z']}

    cost_func = BasicDirectedLinkCostFunction(parameters=parameters)

    trajs = data.brownian_trajs_df()
    times_stamp = trajs.index.get_level_values('t_stamp').unique()

    t0 = times_stamp[3]
    t1 = times_stamp[4]
    pos0 = trajs.ix[t0]
    pos1 = trajs.ix[t1]

    cost_func.context['pos_in'] = pos0
    cost_func.context['pos_out'] = pos1
    cost_func.context['trajs'] = trajs

    block = cost_func.get_block()

    # To finish
    assert True
