import numpy as np


def get_scores_on_trajectories(trajs, coords=['x', 'y', 'z']):
    """

    Parameters
    ----------
    trajs : pd.DataFrame
        MultiIndex need to contain 't_stamp' and 'label' and columns need to have at least
        'true_label'
    coords : list
        Features on which process scoring.

    Returns
    -------
    min_chi_square : float
    conserved_trajectories_number : float
        Between 0 and 1.
    scores : numpy.ndarray
        Chi square matrix.
    """
    gp_new = trajs.groupby(level='label').groups
    gp_true = trajs.groupby('true_label').groups

    scores = np.empty((len(gp_new), len(gp_true)))

    for new_label, new_id in gp_new.items():
        for true_label, true_id in gp_true.items():

            p = trajs.loc[new_id]
            h = trajs.loc[true_id]

            p = p.reset_index(level='label')
            h = h.reset_index(level='label')
            h = h.reindex_like(p)

            h.dropna(inplace=True)

            score = ((h - p)[['x', 'y', 'z']].sum(axis=1) ** 2).mean()
            scores[new_label, true_label] = score

    min_chi_square = np.min(scores, axis=1).sum()
    conserved_trajectories_number = scores.shape[1] / scores.shape[0]

    return min_chi_square, conserved_trajectories_number, scores
