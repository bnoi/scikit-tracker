import logging
import os
import pandas as pd

log = logging.getLogger(__name__)
from .io import validate_metadata

class ObjectsIO():
    """
    class used to manipulate and pass along data issued from detected
    objects
    """

    def __init__(self, metadata=None,
                 store_path=None, base_dir=None):

        self.metadata = metadata
        validate_metadata(metadata)
        self.base_dir = base_dir
        
        if store_path is None:
            store_name = metadata['FileName'].split(os.path.sep)[-1]
            store_name = store_name.split('.')[0]+'.h5'
            store_path = os.path.join(os.path.dirname(metadata['FileName']),
                                      store_name)
        if base_dir is None:
            self.store_path = store_path
            self.image_path = metadata['FileName']
        else:
            self.store_path = os.path.join(base_dir, store_path)
            self.image_path = os.path.join(base_dir, metadata['FileName'])

    @classmethod
    def from_h5(cls, store_path, base_dir=''):
        
        store_path = os.path.join(base_dir, store_path)
        with pd.get_store(store_path) as store:
            metadata_serie = store['metadata']
        metadata = metadata_serie.to_dict()
        validate_metadata(metadata)
        return cls.__init__(metadata=metadata,
                            store_path=store_path,
                            base_dir=base_dir)

    def save_metadata(self):
        with pd.get_store(self.store_path) as store:
            store['metadata'] = _serialize(self.metadata)
            
            
def _serialize(attr):
    ''' Creates a pandas series from a dictionnary'''
    return pd.Series(list(attr.values()), index=attr.keys())