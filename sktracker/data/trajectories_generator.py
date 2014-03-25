import numpy as np
import pandas as pd


def trajectories_generator(n_part=5,
                           n_times=100,
                           noise=1e-10,
                           p_disapear=1e-10,
                           sampling=10,
                           seed=0):
    """Build and return fake trajectories with x, y, z and t features.

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

    """

    if seed:
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

    trajs['true_label'] = trajs.index.get_level_values(1)

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
    sampling *= 2. * np.pi
    xs = times * np.cos(times / sampling + phase)
    ys = np.sin(times / sampling - phase)**2
    zs = times / 10.
    xs /= xs.ptp()
    ys /= ys.ptp()
    zs /= zs.ptp()

    return np.array([xs, ys - ys[0], zs]).T
