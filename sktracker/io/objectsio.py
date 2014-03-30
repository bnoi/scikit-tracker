import logging
import os
import xml.etree.cElementTree as et

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

from . import StackIO
from . import validate_metadata

__all__ = []


class ObjectsIO():
    """
    Manipulate and pass along data issued from detected
    objects.

    Parameters
    ----------
    metadata : dict
        Metadata related to an image or images list.
    store_path : str
        Path to HDF5 file where metadata and objects are stored.
    base_dir : str
        Root directory (join to find `store_path`)

    """

    def __init__(self, metadata=None,
                 store_path=None,
                 base_dir=None):

        self.metadata = metadata
        validate_metadata(metadata)
        self.base_dir = base_dir

        if store_path is None:
            store_name = metadata['FileName'].split(os.path.sep)[-1]
            store_name = store_name.split('.')[0] + '.h5'
            store_path = os.path.join(os.path.dirname(metadata['FileName']),
                                      store_name)
        if base_dir is None:
            self.store_path = store_path
            self.image_path = metadata['FileName']
        else:
            self.store_path = os.path.join(base_dir, store_path)
            self.image_path = os.path.join(base_dir, metadata['FileName'])

        self.__setitem__('metadata', _serialize(self.metadata))

    def __getitem__(self, name):
        """Get an object from HDF5 file.

        Parameters
        ----------
        name : str
            Name of the object. Will be used when reading HDF5 file

        """
        with pd.get_store(self.store_path) as store:
            obj = store[name]

        if isinstance(obj, pd.Series):
            return obj.to_dict()
        else:
            return obj

    def __setitem__(self, name, obj):
        """Add an object to HDF5 file.

        Parameters
        ----------
        obj : object
            :class:`pandas.DataFrame`, :class:`pandas.Series` or dict
        name : str
            Name of the object. Will be used when reading HDF5 file

        """
        with pd.get_store(self.store_path) as store:
            if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
                store[name] = obj
            elif isinstance(obj, dict):
                store[name] = _serialize(obj)

    def __delitem__(self, name):
        """
        """
        with pd.get_store(self.store_path) as store:
            store.remove('name')

    def keys(self):
        """Return list of objects in HDF5 file.
        """

        objs = []
        with pd.get_store(self.store_path) as store:
            objs = store.keys()
        return objs

    @classmethod
    def from_h5(cls, store_path, base_dir=None):
        """Load ObjectsIO from HDF5 file.

        Parameters
        ----------
        store_path : str
            HDF5 file path.
        base_dir : str
            Root directory

        """

        if base_dir:
            full_store_path = os.path.join(base_dir, store_path)
        else:
            full_store_path = store_path

        with pd.get_store(full_store_path) as store:
            metadata_serie = store['metadata']

        metadata = metadata_serie.to_dict()
        validate_metadata(metadata)

        return cls(metadata=metadata,
                   store_path=store_path,
                   base_dir=base_dir)

    @classmethod
    def from_trackmate_xml(cls, trackmate_xml_path):
        """Load ObjectsIO from TrackMate XML.

        Parameters
        ----------
        trackmate_xml_path : str
            TrackMate XML file path.
        """

        root = et.fromstring(open(trackmate_xml_path).read())
        image_data = root.find('Settings').find('ImageData')

        filename = image_data.get('filename')
        folder = image_data.get('folder')

        st = StackIO(filename, base_dir=folder)
        metadata = st.metadata

        validate_metadata(metadata)

        oio = cls(metadata=metadata, base_dir=folder)

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

        oio['trajs'] = trajs
        return oio


def _serialize(attr):
    ''' Creates a pandas series from a dictionnary'''
    return pd.Series(list(attr.values()), index=attr.keys())