from numpy.testing import assert_array_equal

from sktracker.tracker.lapjv import lapjv


def test_lapjv():

    i = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2,
         2, 2, 3, 3, 3, 4, 4, 4, 4, 4,
         5, 5, 5, 5, 5, 6, 6, 7, 7, 8, 8]

    j = [0, 1, 2, 3, 4, 5, 0, 1, 6, 0,
         1, 7, 0, 1, 8, 0, 5, 6, 7, 8,
         1, 5, 6, 7, 8, 2, 5, 3, 5, 4, 5]

    costs = [1., 1., 1., 1., 1., 1.,
             1., 1., 1., 1., 1., 1.,
             1., 1., 1., 1., 2., 2.,
             2., 2., 1., 2., 2., 2.,
             2., 1., 2., 1., 2., 1., 2.]

    in_links, out_links = lapjv(i, j, costs)

    assert_array_equal(in_links, [5, 6, 7, 8, 0, 1, 2, 3, 4])
    assert_array_equal(out_links, [4, 5, 6, 7, 8, 0, 1, 2, 3])
