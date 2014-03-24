import logging

import pandas as pd

log = logging.getLogger(__name__)
from .io import validate_metadata

class ObjectsIO():
    """
    class used to manipulate and pass along data issued from detected
    objects
    """

    def __init__(self, objects_df=None, metadata=None, store_path=None):

        self.objects = objects_df
        self.metadata = metadata
        self.store_path = store_path

    @classmethod
    def from_h5(cls, store_path):
        with pd.get_store(store_path) as store:
            metadata_serie = store['metadata']
            objects_df = store['objects']

        metadata_dict = metadata_serie.to_dict()
        validate_metadata(metadata_dict)
        return cls.__init__(objects_df=objects_df,
                            metadata=metadata_dict,
                            store_path=store_path)

    def save_h5(self):
        
        with pd.get_store(self.store_path) as store:
            store['metadata'] = _serialize(self.metadata)
            store['objects'] = self.objects


            
def _serialize(attr):
    ''' Creates a pandas series from a dictionnary'''
    return pd.Series(list(attr.values()), index=attr.keys())