
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
import pandas as pd
from pandas.io import pytables
from scipy.interpolate import splev, splrep



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
        return self.index.get_level_values('label').unique().astype(np.int)

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

    def get_mean_distances(self, group_args={'by': 'true_label'},
                           coords=['x', 'y', 'z']):
        """Return the mean distances between each timepoints. Objects are grouped
        following group_args parameters.

        Parameters
        ----------
        group_args : dict
            Used to group objects with :meth:`pandas.DataFrame.groupby`.
        coords : list
            Column names used to compute euclidean distance.

        Returns
        -------
        mean_dist : :class:`pandas.DataFrame`
        """

        def get_euclidean_distance(vec):
            vec = vec.loc[:, coords].values
            dist = (vec[:-1] - vec[1:]) ** 2
            dist = dist.sum(axis=-1)
            dist = np.sqrt(dist)
            return pd.DataFrame(dist, columns=['distance'])

        groups = self.groupby(**group_args)
        distances = groups.apply(get_euclidean_distance)
        mean_dist = distances.groupby(level=0).mean()

        return mean_dist

    def show(self, xaxis='t',
             yaxis='x',
             groupby_args={'level': "label"},
             ax=None, **kwargs):  # pragma: no cover
        """Show trajectories

        Parameters
        ----------
        xaxis : str
        yaxis : str
        groupby : dict
            How to group trajectories
        ax : :class:`matplotlib.axes.Axes`
            None will create a new one.
        **kwargs are passed to the plot function

        Returns
        -------
        :class:`matplotlib.axes.Axes`

        Examples
        --------
        >>> from sktracker import data
        >>> from sktracker.tracker.solver import ByFrameSolver
        >>> import matplotlib.pylab as plt
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
        colors = self.get_colors()
        gp = self.groupby(**groupby_args).groups

        ### Set default kwargs if they are not provided
        ### Unfortunately you can't pass somthing as '-o'
        ### as a single linestyle kwarg

        if ((kwargs.get('ls') is None)
           and (kwargs.get('linestyle') is None)):
            kwargs['ls'] = '-'
        if kwargs.get('marker') is None:
            kwargs['marker'] = 'o'
        if ((kwargs.get('c') is None)
            and (kwargs.get('color') is None)):
            auto_color = True
        else:
            auto_color = False

        for k, v in gp.items():
            traj = self.loc[v]
            if auto_color:
                c = colors[v[0][1]]  # that's the label
                kwargs['color'] = c
            ax.plot(traj[xaxis], traj[yaxis], **kwargs)

        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)
        ax.set_title(str(groupby_args))

        return ax

    def get_colors(self):
        import matplotlib.pyplot as plt
        ccycle = plt.rcParams['axes.color_cycle']
        num_colors = len(ccycle)
        clrs = {}
        for label in self.labels:
            clrs[label] = ccycle[label % num_colors]
        return clrs


    def time_interpolate(self, time_step=None,
                         coords=('x', 'y', 'z'), s=0, k=3):
        """
        Interpolates each segment of the trajectories along time
        using `scipy.interpolate.splrep`

        Parameters
        ----------
        time_step : np.float or None, default None
           the time step between the interpolated trajectory
           if this is `None`, it is computed as the minimum non null
           time difference between two points in the trajectory
        coords : tuple of column names, default `('x', 'y', 'z')`
           the coordinates to interpolate.
         s : float
            A smoothing condition. The amount of smoothness is determined by
            satisfying the conditions: sum((w * (y - g))**2,axis=0) <= s where g(x)
            is the smoothed interpolation of (x,y). The user can use s to control
            the tradeoff between closeness and smoothness of fit. Larger s means
            more smoothing while smaller values of s indicate less smoothing.
            Recommended values of s depend on the weights, w. If the weights
            represent the inverse of the standard-deviation of y, then a good s
            value should be found in the range (m-sqrt(2*m),m+sqrt(2*m)) where m is
            the number of datapoints in x, y, and w. default : s=m-sqrt(2*m) if
            weights are supplied. s = 0.0 (interpolating) if no weights are
            supplied.
        k : int
           The order of the spline fit. It is recommended to use cubic splines.
           Even order splines should be avoided especially with small s values.
           1 <= k <= 5

        Returns
        -------
        interpolated : a :class:`Trajectories` instance
           The interpolated values with column names identical to `ccords`
           plus the computed speeds (first order derivative) and accelarations
           (second order derivative) if `k` > 2

        Notes
        -----
        The `s` and `k` arguments are passed to `scipy.interpolate.splrep`, see this
             function documentation for more details
        If a segment is too short to be interpolated with the passed order `k`, the order
             will be automatically diminished
        Segments with only one point will be returned as is


        """
        interpolated = {}
        if time_step is None:
            self.sort('t', inplace=True)
            dts = self.t.diff().dropna().unique()
            time_step = dts[dts != 0].min()

        for label, segment in self.iter_segments:
            if segment.shape[0] < 2:
                interpolated[label] = segment[coords+'t']
            corrected_k = k
            while segment.shape[0] <= corrected_k:
                corrected_k -= 1
            tck = _spline_rep(segment, coords, s=s, k=corrected_k)
            t0, t1 = segment.t.iloc[0], segment.t.iloc[-1]
            t_span =  t1 - t0
            n_pts = np.floor(t_span / time_step) + 1
            times = np.linspace(t0, t1, n_pts)
            tmp_df = pd.DataFrame(index=np.arange(times.size))
            tmp_df['t'] = times
            for coord in coords:
                tmp_df[coord] = splev(times, tck[coord], der=0)
                tmp_df['v_'+coord] = splev(times, tck[coord], der=1)
                if k > 2:
                    if corrected_k > 2:
                        tmp_df['a_'+coord] = splev(times, tck[coord], der=2)
                    else:
                        tmp_df['a_'+coord] = times * np.nan

            interpolated[label] = tmp_df
        interpolated = pd.concat(interpolated)
        interpolated.index.names = 'label', 't_stamp'
        interpolated = interpolated.swaplevel('label', 't_stamp')
        return Trajectories(interpolated)

# Register the trajectories for storing in HDFStore
# as a regular DataFrame
pytables._TYPE_MAP[Trajectories] = 'frame'



def _spline_rep(df, coords=('x', 'y', 'z'), s=0, k=3):
    time = df.t
    tcks = {}
    for coord in coords:
        tcks[coord] = splrep(time, df[coord].values, s=s, k=k)
    return pd.DataFrame.from_dict(tcks)

