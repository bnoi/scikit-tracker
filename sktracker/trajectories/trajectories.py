import numpy as np
import pandas as pd

__all__ = []


class Trajectories(pd.DataFrame):
    """
    This class is a subclass of the class :class:`pandas.DataFrame`

    It is mainly here to provide utility attributes and syntactic shugar.

    Attributes
    ----------
    t_stamps : ndarray
        unique values of the `t_stamps` index of `self.trajs`

    labels : ndarray
        unique values of the `labels` index of `self.trajs`

    iter_segments : iterator
        yields a `(label, segment)` pair where `label` is iterated over `self.labels`
        and `segment` is a chunk of `self.trajs`

    segment_idxs : dictionnary
        Keys are the segent label and values are a list
        of  `(t_stamp, label)` tuples for each time point of the segment

    Parameters
    ----------
    trajs : :class:`pandas.DataFrame`

    """
    def __init__(self, trajs):

        if not isinstance(trajs, pd.DataFrame):
            raise TypeError("The constructor argument `trajs` "
                            "must be a pandas.DataFrame instance")
        super().__init__(trajs)

    @property
    def t_stamps(self):
        return self.index.get_level_values('t_stamp').unique()

    @property
    def labels(self):
        return self.index.get_level_values('label').unique()

    @property
    def segment_idxs(self):
        return self.groupby(level='label').groups

    @property
    def iter_segments(self):
        for lbl, idxs in self.segment_idxs.items():
            yield lbl, self.loc[idxs]

    def get_segments(self):
        """A segment contains all the data from `self.trajs` with

        Returns
        -------
        A dict with labels as keys and segments as values
        """
        return {key: segment for key, segment
                in self.iter_segments}

    def reverse(self):
        """Reverse trajectories.

        Returns
        -------
        A copy of current :class:`sktracker.trajectories.Trajectories`
        """

        trajs = self.copy()
        trajs.reset_index(inplace=True)
        trajs['t_stamp'] = trajs['t_stamp'] * -1
        trajs['t'] = trajs['t'] * -1
        trajs.sort('t_stamp', inplace=True)
        trajs.set_index(['t_stamp', 'label'], inplace=True)
        return trajs

    def copy(self):
        """
        """

        trajs = super().copy()
        return Trajectories(trajs)

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
        """
        Parameters
        ----------
        level : str
        inplace : bool

        Returns
        -------
        trajs
        """

        old_lbls = self.index.get_level_values(level)
        nu_lbls = old_lbls.values.astype(np.uint16).copy()
        for n, uv in enumerate(old_lbls.unique()):
            nu_lbls[old_lbls == uv] = n

        if not inplace:
            trajs = self.copy()
        else:
            trajs = self

        trajs['new_label'] = nu_lbls
        trajs.set_index('new_label', append=True, inplace=True)
        trajs.reset_index(level, drop=True, inplace=True)
        names = list(self.index.names)
        names[names.index('new_label')] = level
        trajs.index.set_names(names, inplace=True)
        return trajs

    def show(self, xaxis='t',
             yaxis='x',
             groupby_args={'level': "label"},
             shape='-o',
             ax=None):  # pragma: no cover
        """Show trajectories

        Parameters
        ----------
        xaxis : str
        yaxis : str
        groupby : dict
            How to group trajectories
        ax : :class:`matplotlib.axes.Axes`
            None will create a new one.

        Returns
        -------
        :class:`matplotlib.axes.Axes`

        Examples
        --------
        >>> from sktracker import data
        >>> from sktracker.tracker.solver import ByFrameSolver
        >>> true_trajs = data.brownian_trajectories_generator(p_disapear=0.1)
        >>> solver = ByFrameSolver.for_brownian_motion(true_trajs, max_speed=2)
        >>> trajs = solver.track(progress_bar=False)
        >>> fig, (ax1, ax2) = plt.subplots(nrows=2)
        >>> ax1 = trajs.show(xaxis='t', yaxis='x', groupby_args={'level': "label"}, ax=ax1)
        >>> ax2 = trajs.show(xaxis='t', yaxis='x', groupby_args={'by': "true_label"}, ax=ax2)

        """

        import matplotlib.pyplot as plt

        if ax is None:
            ax = plt.gca()

        gp = self.groupby(**groupby_args).groups
        for k, v in gp.items():
            traj = self.loc[v]
            ax.plot(traj[xaxis], traj[yaxis], shape)

        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)
        ax.set_title(str(groupby_args))

        return ax
