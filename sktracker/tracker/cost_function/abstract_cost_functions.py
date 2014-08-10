# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import pandas as pd

__all__ = []


class AbstractCostFunction(object):
    """Abstract class

    Parameters
    ----------
    context : dict
    parameters : dict
    """

    def __init__(self, context, parameters):
        self.context = context
        self.parameters = parameters

    def get_block(self, *args, **kwargs):
        """This method will update the values in `self.mat`. It should be overwritten for any matrix
        verification returned by self.build.


        """
        self.mat = self._build(*args, **kwargs)

    def _build(self):
        """This method needs to be overwritten by subclasses
        """
        return None

    def check_columns(self, objects, cols):
        """Check pandas.DataFrame column names.

        Parameters
        ----------
        objects : list of :class:`pandas.DataFrame` or :class:`pandas.DataFrame`
        cols : list column names to check
        """

        if isinstance(objects, pd.DataFrame):
            objects = [objects]

        cols_set = set(cols)
        for obj in objects:
            actual_cols_set = set(obj.columns.values)
            if not cols_set.issubset(actual_cols_set):
                raise ValueError("The passed dataframe doesn't"
                                 " contain the required columns."
                                 "Missing columns: {}".format(
                                     cols_set.difference(actual_cols_set)))

    def check_context(self, key, obj_type):
        """Check wether self.context contain a key on a specific type.

        Parameters
        ----------
        key : str
            Key to find in self.context.
        obj_type : class name
            To check context value type.

        Returns
        -------
        The desired key's value in context.
        """

        message = "Context {} does not contain required key : {}"
        if key not in self.context.keys():
            raise ValueError(message.format(self.context, key))

        message = "Context value {} does not have valid key type : {}"
        if not isinstance(self.context[key], obj_type):
            raise TypeError(message.format(self.context[key], obj_type))

        return self.context[key]
