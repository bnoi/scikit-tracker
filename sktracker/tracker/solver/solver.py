
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


from ...trajectories import Trajectories

__all__ = []


class AbstractSolver:
    """

    Parameters
    ----------
    trajs : :class:`sktracker.trajectories.Trajectories`
        The trajectories
    """

    def __init__(self, trajs):
        self.trajs = Trajectories(trajs)

    def check_cost_function_type(self, obj, cost_funtion_type):
        """Check wether an object inherit from another one.

        Parameters
        ----------
        obj : object
        cost_funtion_type : class name

        Raises
        ------
        TypeError : `obj` type does not inherit from `cost_funtion_type`
        """

        error_mess = '''The cost function {} doesn't inherit from {}'''

        if not isinstance(obj, cost_funtion_type):
            raise TypeError(error_mess.format(obj, cost_funtion_type.__name__))

    def relabel_trajs(self, new_labels=None):
        """
        Sets the trajectory index `label` to new values.

        Parameters
        ----------
        new_labels: :class:`numpy.ndarray` or None, default None
            The new label. If it is not provided, the function wil look for
            will look for a column named "new_label" in `trajs` and use this
            as the new label index

        """
        if new_labels is not None:
            self.trajs['new_label'] = new_labels

        try:
            self.trajs.set_index('new_label', append=True, inplace=True)
        except KeyError:
            raise('''Column "new_label" was not found in `trajs` and none
                      was provided''')

        self.trajs.reset_index(level='label', drop=True, inplace=True)
        self.trajs.index.set_names(['t_stamp', 'label'], inplace=True)
        self.trajs.sortlevel('label', inplace=True)
        self.trajs.sortlevel('t_stamp', inplace=True)
        self.trajs.relabel_fromzero('label', inplace=True)
