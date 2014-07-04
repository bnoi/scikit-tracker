# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


'''
in the sence of sklearn.decomposition

'''

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from ..trajectories import Trajectories

import logging
log = logging.getLogger(__name__)

def do_pca(trajs,
           pca=None,
           coords=['x', 'y', 'z'],
           suffix='',
           append=False, return_pca=False):
    '''
    Performs a principal component analysis on the input coordinates
    '''
    if pca is None:
        pca = PCA()
    pca_coords = [c + suffix for c in coords]
    if not np.all(np.isfinite(trajs[coords])):
        log.warning('''Droping non finite values before performing PCA''')

    rotated_ = pd.DataFrame(pca.fit_transform(trajs[coords].dropna()))
    rotated_.set_index(trajs[coords].dropna().index, inplace=True)
    rotated = pd.DataFrame(columns=pca_coords,
                           index=trajs.index)
    rotated.loc[rotated_.index] = rotated_
    rotated['t'] = trajs.t

    rotated.reindex_like(trajs)
    if append:
        for pca_coord in pca_coords:
            trajs[pca_coord] = rotated[pca_coord]
        if return_pca:
            return trajs, pca
        else:
            return trajs

    if return_pca:
        return Trajectories(rotated), pca
    else:
        return Trajectories(rotated)
