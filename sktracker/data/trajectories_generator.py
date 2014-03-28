import numpy as np
import pandas as pd


def brownian_trajectories_generator(n_part=5,
                                    n_times=100,
                                    p_disapear=0,
                                    sigma=1.,
                                    init_dispersion=10.,
                                    seed=None):
    """Build and return fake brownian trajectories with x, y, z and t features.

    Parameters
    ----------
    n_part : int
        Number of trajectories
    n_times : int
        Number of time points
    p_disapear : float
        Probability that a particle disapears in one frame
    sigma : float
        Brownian motion parameters.
    init_dispersion : float
        Initial dispersion amplitude.
    seed : float
        See value for random function.

    Returns
    -------
    trajs : `pandas.DataFrame`
        Simulated trajectories. Column named `true_label` contains correct
        object labels.

    """
    if seed is not None:
        np.random.seed(seed)

    init_dispersion *= sigma
    time_stamps, labels = np.mgrid[:n_times, :n_part]

    positions = np.random.normal(scale=sigma,
                                 size=(n_times, n_part, 3))
    init_pos = np.random.normal(scale=init_dispersion,
                                size=(n_part, 3))
    positions[0, ...] = init_pos
    positions = positions.cumsum(axis=0)

    index = pd.MultiIndex.from_arrays([time_stamps.flatten(),
                                       labels.flatten()],
                                      names=('t_stamp', 'label'))

    trajs = pd.DataFrame(positions.reshape(n_times*n_part, 3),
                         index=index, columns=['x', 'y', 'z'])

    disapear = np.random.binomial(n_part, p_disapear, n_times * n_part)
    disapear = np.where(disapear == 1)[::-1][0]
    if disapear.size > 0:
        trajs = trajs.drop(trajs.index[disapear])

    trajs['true_label'] = trajs.index.get_level_values(1)

    grouped = trajs.groupby(level='t_stamp')
    trajs = grouped.apply(_shuffle)

    trajs['t'] = trajs.index.get_level_values('t_stamp').values.astype(np.float)
    return trajs


def directed_trajectories_generator(n_part=5,
                                    n_times=100,
                                    noise=1e-10,
                                    p_disapear=1e-10,
                                    sampling=100,
                                    seed=None):
    """Build and return fake directed trajectories with x, y, z and t features.

    Parameters
    ----------
    n_part : int
        Number of trajectories
    n_times : int
        Number of time points
    noise: float
        Typical position noise
    p_disapear : float
        Probability that a particle disapears in one frame
    sampling : int
        Typical density of points w/r to trajectories
        variations. This corresponds typicaly to the number of points
        for one period of an oscillating function.
    seed : float
        See value for random function.

    Returns
    -------
    trajs : `pandas.DataFrame`
        Simulated trajectories. Column named `true_label` contains correct
        object labels.

    Examples
    --------

    >>> trajs = data.trajectories_generator(n_part=5, n_times=100,
                                            noise=1e-10, p_disapear=1e-10,
                                            sampling=10, seed=0)
    >>> print(trajs)
                              x         y         z  true_label   t
        t_stamp label
        0       0      0.616882  0.902349  0.521563           4   0
                1      0.153268  0.963879  0.641001           0   0
                2      0.697661  0.765814  0.952269           2   0
                3      0.133093  0.616393  0.119415           3   0
                4      0.580687  0.054081  0.465635           1   0
        1       0      0.120437  0.639993  0.129516           3   1
                1      0.712195  0.785034  0.962370           2   1
                2      0.625566  0.870682  0.531664           4   1
                3      0.577739  0.043900  0.475736           1   1
                4      0.135332  0.976875  0.651102           0   1
        2       0      0.633960  0.839042  0.541765           4   2
                1      0.107496  0.663800  0.139617           3   2
                2      0.726992  0.804561  0.972471           2   2
                3      0.117182  0.990282  0.661203           0   2
                4      0.575109  0.033273  0.485837           1   2
        ...

    """

    if seed is not None:
        np.random.seed(seed)

    times = np.arange(n_times)
    phases = np.random.random(n_part) * 2 * np.pi
    initial_positions = np.random.random((n_part, 3))
    time_stamps, labels = np.mgrid[:n_times, :n_part]

    index = pd.MultiIndex.from_arrays([time_stamps.flatten(),
                                       labels.flatten()],
                                      names=('t_stamp', 'label'))

    all_pos = np.zeros((n_times * n_part, 3))
    for n in range(n_part):
        phase = phases[n]
        pos0 = initial_positions[n, :]
        pos_err = np.random.normal(0, noise, (n_times, 3))
        all_pos[n::n_part] = (pos0
                              + _positions(times, phase, sampling)
                              + pos_err)

    trajs = pd.DataFrame(all_pos, index, columns=('x', 'y', 'z'))

    disapear = np.random.binomial(n_part, p_disapear, n_times * n_part)
    disapear = np.where(disapear == 1)[::-1][0]
    if disapear.size > 0:
        trajs = trajs.drop(trajs.index[disapear])

    trajs['true_label'] = trajs.index.get_level_values('label')

    grouped = trajs.groupby(level='t_stamp')
    trajs = grouped.apply(_shuffle)

    trajs['t'] = trajs.index.get_level_values('t_stamp').values.astype(np.float)

    return trajs


def _shuffle(df):
    """
    Shuffles the input `pandas.DataFrame` and returns it.
    """
    values = df.values
    np.random.shuffle(values)
    df = pd.DataFrame(values,
                      index=df.index,
                      columns=df.columns)
    return df


def _positions(times, phase, sampling=5):
    """
    Computes a swirly trajectory
    """
    sampling /= 2. * np.pi
    xs = times * np.cos(times / sampling + phase)
    ys = np.sin(times / sampling - phase)**2
    zs = times / 10.
    xs /= xs.ptp()
    ys /= ys.ptp()
    zs /= zs.ptp()

    return np.array([xs, ys - ys[0], zs]).T
