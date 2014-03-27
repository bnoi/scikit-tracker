import numpy as np


def relabel_fromzero(df, level, inplace=False):

    old_lbls = df.index.get_level_values(level)
    nu_lbls = old_lbls.values.astype(np.uint16).copy()
    for n, uv in enumerate(old_lbls.unique()):
        nu_lbls[old_lbls == uv] = n
    if not inplace:
        df = df.copy()
    df['new_label'] = nu_lbls
    df.set_index('new_label', append=True, inplace=True)
    df.reset_index(level, drop=True, inplace=True)
    names = list(df.index.names)
    names[names.index('new_label')] = level
    df.index.set_names(names, inplace=True)
    return df
