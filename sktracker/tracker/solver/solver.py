from ...utils.dataframes import relabel_fromzero


class AbstractSolver:
    """

    Parameters
    ----------
    trajs : pandas.DataFrame
        Trajectories
    """

    def __init__(self, trajs):

        self.trajs = trajs.copy()

    @property
    def pos_in(self):
        return self.trajs.loc[self.t_in]

    @property
    def pos_out(self):
        return self.trajs.loc[self.t_out]

    @property
    def times(self):
        return self.trajs.index.get_level_values('t_stamp').unique()

    def check_trajs_df_structure(self, index=None, columns=None):
        """Check wether trajcetories contains a specified structure.

        Parameters
        ----------
        index : list
            Index names (order is important)
        columns : list
            Column names (order does not matter here)

        Raises
        ------
        ValueError in both case
        """

        error_mess = "Trajectories does not contain correct indexes : {}"
        if index and self.trajs.index.names != index:
            raise ValueError(error_mess.format(index))

        error_mess = "Trajectories does not contain correct columns : {}"
        if columns:
            columns = set(columns)
            if not columns.issubset(set(self.trajs.columns)):
                raise ValueError(error_mess.format(columns))

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
        relabel_fromzero(self.trajs, 'label', inplace=True)
