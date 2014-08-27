import xml.etree.cElementTree as et

import pandas as pd
import numpy as np


def trackmate_peak_import(trackmate_xml_path):
    """Import detected peaks with TrackMate Fiji plugin.

    Parameters
    ----------
    trackmate_xml_path : str
        TrackMate XML file path.
    """

    root = et.fromstring(open(trackmate_xml_path).read())

    objects = []
    object_labels = {'FRAME': 't_stamp',
                     'POSITION_T': 't',
                     'POSITION_X': 'x',
                     'POSITION_Y': 'y',
                     'POSITION_Z': 'z',
                     'MEAN_INTENSITY': 'I',
                     'ESTIMATED_DIAMETER': 'w',
                     'QUALITY': 'q'}

    features = root.find('Model').find('FeatureDeclarations').find('SpotFeatures')
    features = [c.get('feature') for c in features.getchildren()]

    spots = root.find('Model').find('AllSpots')
    trajs = pd.DataFrame([])
    objects = []
    for frame in spots.findall('SpotsInFrame'):
        for spot in frame.findall('Spot'):

            single_object = []
            for label in features:
                single_object.append(spot.get(label))

            objects.append(single_object)
    trajs = pd.DataFrame(objects, columns=features)
    trajs = trajs.astype(np.float)

    # Apply filters
    spot_filters = root.find("Settings").find("SpotFilterCollection")

    for spot_filter in spot_filters.findall('Filter'):
        name = spot_filter.get('feature')
        value = float(spot_filter.get('value'))
        isabove = True if spot_filter.get('isabove') == 'true' else False

        if isabove:
            trajs = trajs[trajs[name] > value]
        else:
            trajs = trajs[trajs[name] < value]

    trajs = trajs.loc[:, object_labels.keys()]
    trajs.columns = [object_labels[k] for k in object_labels.keys()]
    trajs['label'] = np.arange(trajs.shape[0])
    trajs.set_index(['t_stamp', 'label'], inplace=True)

    return trajs
