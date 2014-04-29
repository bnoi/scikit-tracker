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

    # Get detected spots from XML file
    objects = []
    object_labels = [('t_stamp', 'FRAME'),
                     ('t', 'POSITION_T'),
                     ('x', 'POSITION_X'),
                     ('y', 'POSITION_Y'),
                     ('z', 'POSITION_Z'),
                     ('I', 'MEAN_INTENSITY'),
                     ('w', 'ESTIMATED_DIAMETER')]

    spots = root.find('Model').find('AllSpots')
    for frame in spots.findall('SpotsInFrame'):
        for spot in frame.findall('Spot'):

            single_object = []
            for label, trackmate_label in object_labels:
                single_object.append(spot.get(trackmate_label))

            objects.append(single_object)

    trajs = pd.DataFrame(objects, columns=[label[0] for label in object_labels])
    trajs['label'] = np.arange(trajs.shape[0])
    trajs['t_stamp'] = trajs['t_stamp'].values.astype(np.float)
    trajs.set_index(['t_stamp', 'label'], inplace=True)
    trajs = trajs.astype(np.float)

    return trajs
