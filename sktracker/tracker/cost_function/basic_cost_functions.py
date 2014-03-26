from collections import defaultdict

import numpy as np

class CostFunction:
    """Abstract class.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """

    DEFAULT_PARAMETERS = {}

    def __init__(self, context, parameters):
        self.context = context

        # self.parameters = DEFAULT_PARAMETERS.copy()
        # self.parameters.update(parameters)

    def build(self):
        """
        """
        pass

class LinkCostFunction(CostFunction):
    """Basic cost function.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """

    DEFAULT_PARAMETERS = {}

    def __init__(self, context, parameters):
        super().__init__(context, parameters)

    def build(self, objects_in, objects_out):
        """
        """
        mat = np.zeros((len(objects_in), len(objects_out)))
        return mat

class DiagCostFunction(CostFunction):
    """Basic cost function for diagonal block.

    Parameters
    ----------
    context : dict
    parameters : dict
        Missing parameters will be filled by DEFAULT_PARAMETERS
    """

    DEFAULT_PARAMETERS = {}

    def __init__(self, context, parameters):
        super().__init__(context, parameters)

    def build(self, objects):
        """
        """
        vec = np.zeros(len(objects))
        return vec
