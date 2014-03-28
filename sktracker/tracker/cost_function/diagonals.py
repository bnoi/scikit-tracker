import numpy as np
from . import AbstractDiagCostFunction


class DiagCostFunction(AbstractDiagCostFunction):
    """Basic cost function for a diagonal block.

    Parameters
    ----------
    context: `dict`
       this dictionnary must contain at least a `cost` key
    """

    def __init__(self, context):
        super().__init__(context, {})
        if not 'cost' in context.keys():
            raise ValueError('''The class DiagCostFunction requires '''
                             '''the `context` dictionnary to contain a `cost` key''')

    def build(self, objects):
        """
        Returns a vector with shape `(len(objects))` filled by
        the value of `self.context['cost']`

        Parameters
        ----------
        `object`: sequence
            The object to which corresponds this diagonal cost
        """
        vect = np.ones(len(objects)) * self.context['cost']
        return vect
