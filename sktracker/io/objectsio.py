import logging
import os
import pandas as pd

log = logging.getLogger(__name__)
from . import validate_metadata


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
            `pandas.DataFrame`, `pandas.Series` or dict
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


def _serialize(attr):
    ''' Creates a pandas series from a dictionnary'''
    return pd.Series(list(attr.values()), index=attr.keys())
