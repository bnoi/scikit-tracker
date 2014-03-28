import numpy as np
import pandas as pd


class Trajectories(pd.DataFrame):
    """
    This class is a subclass of the class :class:`pandas.DataFrame`

    It is mainly here to provide utility attributes and syntactic shugar.

    Attributes
    ----------
    t_stamps : ndarray
        unique values of the `t_stamps` index of the `self.trajs` dataframe
    
    labels : ndarray
        unique values of the `labels` index of the `self.trajs` dataframe

    iter_segments : iterator
        yields a `(label, segment)` pair where `label` is iterated over `self.labels`
        and `segment` is a chunk of `self.trajs`
    
    """
    def __init__(self, trajs):

        super().__init__(trajs)
        if not isinstance(self, pd.DataFrame):
            raise TypeError('''The constructor argument `trajs`
                            must be a pandas.DataFrame instance''')
    @property
    def t_stamps(self):
        return self.index.get_level_values('t_stamp').unique()

    @property
    def labels(self):
        return self.index.get_level_values('label').unique()

    @property
    def _segment_idxs(self):
        return self.groupby(level='label').groups

    @property
    def iter_segments(self):
        for lbl, idxs in self._segment_idxs:
            yield lbl, self.loc[idxs]
    
    def get_segments(self):
        """
        Returns a dictionnary with labels as keys and segments as values

        A segment contains all the data from `self.trajs` with 
        
        """
        return {key: segment for key, segment
                in self.iter_segments}

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
        if index and self.index.names != index:
            raise ValueError(error_mess.format(index))

        error_mess = "Trajectories does not contain correct columns : {}"
        if columns:
            columns = set(columns)
            if not columns.issubset(set(self.columns)):
                raise ValueError(error_mess.format(columns))

    def relabel_fromzero(self, level, inplace=False):

        old_lbls = self.index.get_level_values(level)
        nu_lbls = old_lbls.values.astype(np.uint16).copy()
        for n, uv in enumerate(old_lbls.unique()):
            nu_lbls[old_lbls == uv] = n

        if not inplace:
            trajs = Trajectories(self.copy())
        else:
            trajs = self
        trajs['new_label'] = nu_lbls
        trajs.set_index('new_label', append=True, inplace=True)
        trajs.reset_index(level, drop=True, inplace=True)
        names = list(self.index.names)
        names[names.index('new_label')] = level
        trajs.index.set_names(names, inplace=True)
        return trajs
