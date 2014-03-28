from ...trajectories import Trajectories


class AbstractSolver:
    """

    Parameters
    ----------
    trajs : :class:`Trajectories` object
        The trajectories
    """

    def __init__(self, trajs):
        self.trajs = Trajectories(trajs)

    def check_cost_function_type(self, obj, cost_funtion_type):
        """Check wether an object inherit from another one.

        Parameters
        ----------
        obj : object
        cost_funtion_type : class

        Raises
        ------
        TypeError : `obj` type does not inherit from `cost_funtion_type`
        """

        error_mess = ''' The cost function {} doesn't inherit from {}'''

        if not isinstance(obj, cost_funtion_type):
            raise TypeError(error_mess.format(obj, cost_funtion_type.__name__))

    def relabel_trajs(self):
        """Relabel trajectories from zero.
        """

        self.trajs.set_index('new_label', append=True, inplace=True)
        self.trajs.reset_index(level='label', drop=True, inplace=True)
        self.trajs.index.names = ['t_stamp', 'label']
        self.trajs.sortlevel('label', inplace=True)
        self.trajs.sortlevel('t_stamp', inplace=True)
        self.trajs.relabel_fromzero('label', inplace=True)
